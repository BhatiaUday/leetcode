# Start of HEAD
import json
import sys
import math

input_data = json.loads(sys.stdin.read())

map_size = input_data['map_size']
warehouse = [map_size[0] / 2, map_size[1] / 2]
drones = input_data['drones']
deliveries = input_data['deliveries']
no_fly_zones = input_data.get('no_fly_zones', [])
charging_stations = input_data.get('charging_stations', [])
# End of HEAD

# Start of BODY
def solve(warehouse, drones, deliveries, no_fly_zones, charging_stations):
    """
    Schedule drone deliveries to maximize on-time deliveries
    while minimizing energy and makespan.

    Score: on_time_deliveries * 100 - total_energy * 0.1 - makespan * 0.05
    """
    from itertools import permutations

    BATTERY_CAP = 500.0
    CHARGE_RATE = 2.0
    EPS = 1e-9

    wx, wy = warehouse[0], warehouse[1]
    sqrt = math.sqrt

    # -------- Pre-process NFZs into compact tuples for speed --------
    # circle:    (0, T_start, T_end, cx, cy, r2, r)
    # rectangle: (1, T_start, T_end, x_min, y_min, x_max, y_max)
    nfzs = []
    for nfz in no_fly_zones:
        ts = float(nfz['T_start'])
        te = float(nfz['T_end'])
        if nfz['shape'] == 'circle':
            cx, cy = nfz['center']
            r = float(nfz['radius'])
            nfzs.append((0, ts, te, float(cx), float(cy), r * r, r))
        else:
            (x1, y1), (x2, y2) = nfz['corners']
            x_min = min(float(x1), float(x2))
            x_max = max(float(x1), float(x2))
            y_min = min(float(y1), float(y2))
            y_max = max(float(y1), float(y2))
            nfzs.append((1, ts, te, x_min, y_min, x_max, y_max))

    def dist(ax, ay, bx, by):
        dx = ax - bx
        dy = ay - by
        return sqrt(dx * dx + dy * dy)

    # ---------------- Segment-vs-NFZ intersection ----------------
    # Returns (hit, T_end). When hit is True, T_end is the NFZ's deactivation
    # time, used to compute the smallest safe wait.
    def seg_nfz(nfz, ax, ay, bx, by, t0, d):
        if d < EPS:
            return False, 0.0
        ts = nfz[1]; te = nfz[2]
        # Traversal window is [t0, t0+d]; NFZ active in [ts, te].
        if t0 + d < ts - EPS or t0 > te + EPS:
            return False, te
        s_lo = (ts - t0) / d
        if s_lo < 0.0:
            s_lo = 0.0
        s_hi = (te - t0) / d
        if s_hi > 1.0:
            s_hi = 1.0
        if s_lo > s_hi + EPS:
            return False, te
        dx = bx - ax
        dy = by - ay
        if nfz[0] == 0:
            cx = nfz[3]; cy = nfz[4]; r2 = nfz[5]
            ex = ax - cx; ey = ay - cy
            A = dx * dx + dy * dy
            B = 2.0 * (ex * dx + ey * dy)
            C = ex * ex + ey * ey - r2
            disc = B * B - 4.0 * A * C
            if disc < 0.0:
                return False, te
            sq = sqrt(disc)
            inv2A = 0.5 / A
            s1 = (-B - sq) * inv2A
            s2 = (-B + sq) * inv2A
            lo = s1 if s1 > s_lo else s_lo
            hi = s2 if s2 < s_hi else s_hi
            return (lo <= hi + EPS), te
        else:
            x_min = nfz[3]; y_min = nfz[4]
            x_max = nfz[5]; y_max = nfz[6]
            if dx > EPS or dx < -EPS:
                sx1 = (x_min - ax) / dx
                sx2 = (x_max - ax) / dx
                if sx1 > sx2:
                    sx1, sx2 = sx2, sx1
            else:
                if x_min - EPS <= ax <= x_max + EPS:
                    sx1 = -1e18; sx2 = 1e18
                else:
                    return False, te
            if dy > EPS or dy < -EPS:
                sy1 = (y_min - ay) / dy
                sy2 = (y_max - ay) / dy
                if sy1 > sy2:
                    sy1, sy2 = sy2, sy1
            else:
                if y_min - EPS <= ay <= y_max + EPS:
                    sy1 = -1e18; sy2 = 1e18
                else:
                    return False, te
            lo = sx1
            if sy1 > lo: lo = sy1
            if s_lo > lo: lo = s_lo
            hi = sx2
            if sy2 < hi: hi = sy2
            if s_hi < hi: hi = s_hi
            return (lo <= hi + EPS), te

    def blocked(ax, ay, bx, by, t0):
        if not nfzs:
            return False
        d = dist(ax, ay, bx, by)
        for nfz in nfzs:
            hit, _ = seg_nfz(nfz, ax, ay, bx, by, t0, d)
            if hit:
                return True
        return False

    # Smallest wait w >= 0 such that the segment departing at t0+w is
    # unblocked. At each step, jump past max(T_end) of all currently
    # blocking NFZs. Each iteration strictly increases t past at least one
    # NFZ's T_end, so it terminates in O(|nfzs|) iterations.
    def get_wait(ax, ay, bx, by, t0):
        if not nfzs:
            return 0.0
        d = dist(ax, ay, bx, by)
        if d < EPS:
            return 0.0
        t = t0
        for _ in range(2 * len(nfzs) + 4):
            max_te = -1.0
            any_hit = False
            for nfz in nfzs:
                hit, te = seg_nfz(nfz, ax, ay, bx, by, t, d)
                if hit:
                    any_hit = True
                    if te > max_te:
                        max_te = te
            if not any_hit:
                return t - t0
            new_t = max_te + 1e-6
            if new_t <= t + EPS:
                return None
            t = new_t
        return None

    # ---------------- Energy estimator for a delivery order ----------------
    def eval_order(order, trip_dels, total_w):
        e = 0.0
        pos_x = wx; pos_y = wy
        w = total_w
        for i in order:
            d = trip_dels[i]
            dp_x = d['x']; dp_y = d['y']
            e += dist(pos_x, pos_y, dp_x, dp_y) * (1.0 + w)
            w -= d['weight']
            pos_x = dp_x; pos_y = dp_y
        e += dist(pos_x, pos_y, wx, wy)
        return e

    def two_opt(order, trip_dels, total_w):
        order = list(order)
        n = len(order)
        if n < 4:
            return tuple(order)
        best_e = eval_order(order, trip_dels, total_w)
        improved = True
        passes = 0
        while improved and passes < 20:
            improved = False
            passes += 1
            for i in range(n - 1):
                for j in range(i + 1, n):
                    new_order = order[:i] + order[i:j + 1][::-1] + order[j + 1:]
                    e = eval_order(new_order, trip_dels, total_w)
                    if e + 1e-9 < best_e:
                        order = new_order
                        best_e = e
                        improved = True
        return tuple(order)

    def best_order(trip_dels):
        n = len(trip_dels)
        total_w = sum(d['weight'] for d in trip_dels)
        if n == 0:
            return ()
        if n == 1:
            return (0,)
        if n <= 7:
            return min(permutations(range(n)),
                       key=lambda o: eval_order(o, trip_dels, total_w))
        # Nearest-neighbor seed + 2-opt refinement.
        rem = set(range(n))
        pos_x = wx; pos_y = wy
        order = []
        while rem:
            best_i = -1; best_d = 1e30
            for i in rem:
                d = trip_dels[i]
                dd = dist(pos_x, pos_y, d['x'], d['y'])
                if dd < best_d:
                    best_d = dd; best_i = i
            order.append(best_i)
            rem.remove(best_i)
            pos_x = trip_dels[best_i]['x']; pos_y = trip_dels[best_i]['y']
        return two_opt(order, trip_dels, total_w)

    # ---------------- Trip simulator ----------------
    def simulate_trip(order, trip_dels, t_start, max_payload):
        path = []
        t = t_start
        bat = BATTERY_CAP
        pos_x = wx; pos_y = wy
        w = sum(d['weight'] for d in trip_dels)
        if w > max_payload + EPS:
            return None

        path.append({
            "x": round(wx, 2), "y": round(wy, 2), "t": round(t, 2),
            "action": "PICKUP",
            "delivery_ids": [trip_dels[i]['id'] for i in order],
        })

        for idx in order:
            d = trip_dels[idx]
            dp_x = d['x']; dp_y = d['y']
            seg = dist(pos_x, pos_y, dp_x, dp_y)
            wt = get_wait(pos_x, pos_y, dp_x, dp_y, t)
            if wt is None:
                return None
            if wt > EPS:
                t += wt
                if t + seg > d['deadline'] + EPS:
                    return None
                path.append({
                    "x": round(pos_x, 2), "y": round(pos_y, 2),
                    "t": round(t, 2), "action": "WAIT",
                })
            energy = seg * (1.0 + w)
            if bat - energy < -EPS:
                return None
            bat -= energy
            t += seg
            if t > d['deadline'] + EPS:
                return None
            path.append({
                "x": round(dp_x, 2), "y": round(dp_y, 2),
                "t": round(t, 2), "action": "DELIVER",
                "delivery_id": d['id'],
            })
            w -= d['weight']
            pos_x = dp_x; pos_y = dp_y

        # ---- Return home, possibly via a charging station ----
        ret_d = dist(pos_x, pos_y, wx, wy)
        ret_energy = ret_d * (1.0 + w)  # w should be ~0 here
        if bat - ret_energy >= -EPS:
            wt = get_wait(pos_x, pos_y, wx, wy, t)
            if wt is None:
                # Try via charging station as a fallback for NFZ avoidance.
                pass
            else:
                if wt > EPS:
                    t += wt
                    path.append({
                        "x": round(pos_x, 2), "y": round(pos_y, 2),
                        "t": round(t, 2), "action": "WAIT",
                    })
                t += ret_d
                bat -= ret_energy
                path.append({
                    "x": round(wx, 2), "y": round(wy, 2),
                    "t": round(t, 2), "action": "RETURN",
                })
                return path, t

        # Need to charge (or detour via station).
        best_plan = None
        best_total_time = float('inf')
        best_cs = None
        for cs in charging_stations:
            cx = cs['x']; cy = cs['y']
            d2cs = dist(pos_x, pos_y, cx, cy)
            e2cs = d2cs * (1.0 + w)
            if bat - e2cs < -EPS:
                continue
            wt1 = get_wait(pos_x, pos_y, cx, cy, t)
            if wt1 is None:
                continue
            t_arrive_cs = t + wt1 + d2cs
            bat_at_cs = bat - e2cs
            d_cw = dist(cx, cy, wx, wy)
            needed_charge = d_cw - bat_at_cs
            if needed_charge < 0.0:
                needed_charge = 0.0
            ct = math.ceil(needed_charge / CHARGE_RATE)
            t_depart_cs = t_arrive_cs + ct
            wt2 = get_wait(cx, cy, wx, wy, t_depart_cs)
            if wt2 is None:
                continue
            total_time = (t_arrive_cs - t) + ct + wt2 + d_cw
            if total_time < best_total_time:
                best_total_time = total_time
                best_cs = cs
                best_plan = (wt1, d2cs, e2cs, t_arrive_cs, bat_at_cs,
                             ct, t_depart_cs, wt2, d_cw)

        if best_cs is None:
            return None

        wt1, d2cs, e2cs, t_arrive_cs, bat_at_cs, ct, t_depart_cs, wt2, d_cw = best_plan
        cx = best_cs['x']; cy = best_cs['y']

        if wt1 > EPS:
            t += wt1
            path.append({
                "x": round(pos_x, 2), "y": round(pos_y, 2),
                "t": round(t, 2), "action": "WAIT",
            })
        bat -= e2cs
        t += d2cs
        path.append({
            "x": round(cx, 2), "y": round(cy, 2),
            "t": round(t, 2), "action": "CHARGE",
        })
        bat += ct * CHARGE_RATE
        if bat > BATTERY_CAP:
            bat = BATTERY_CAP
        t += ct
        path.append({
            "x": round(cx, 2), "y": round(cy, 2),
            "t": round(t, 2), "action": "CHARGE_COMPLETE",
        })
        if wt2 > EPS:
            t += wt2
            path.append({
                "x": round(cx, 2), "y": round(cy, 2),
                "t": round(t, 2), "action": "WAIT",
            })
        bat -= d_cw  # payload 0 on return
        if bat < -EPS:
            return None
        t += d_cw
        path.append({
            "x": round(wx, 2), "y": round(wy, 2),
            "t": round(t, 2), "action": "RETURN",
        })
        return path, t

    # ---------------- Top-level scheduling ----------------
    sorted_dels = sorted(deliveries, key=lambda d: (d['deadline'],
                                                    dist(d['x'], d['y'], wx, wy)))
    assigned = set()
    manifest = []

    for drone in drones:
        did = drone['id']
        mp = float(drone['max_payload'])
        t_now = 0.0
        # Deliveries that this drone has tried-and-failed at the current
        # t_now (e.g., because they're unreachable from here in time/battery).
        # Cleared whenever the drone successfully completes a trip, since
        # t_now changes and so does feasibility.
        skip_for_now = set()

        while True:
            avail = [d for d in sorted_dels if d['id'] not in assigned
                     and d['id'] not in skip_for_now
                     and d['weight'] <= mp + EPS]
            if not avail:
                break

            # Greedy pack by deadline order, respecting payload; cap trip size.
            trip = []
            tw = 0.0
            for d in avail:
                if tw + d['weight'] <= mp + EPS:
                    trip.append(d)
                    tw += d['weight']
                    if len(trip) >= 10:
                        break

            if not trip:
                break

            cache = {}

            def try_trip(cur_trip):
                key = tuple(sorted(d['id'] for d in cur_trip))
                if key in cache:
                    return cache[key]
                order = best_order(cur_trip)
                r = simulate_trip(order, cur_trip, t_now, mp)
                cache[key] = (r, order)
                return cache[key]

            cur = list(trip)
            result = None
            committed_trip = None
            while cur and result is None:
                r, _order = try_trip(cur)
                if r is not None:
                    result = r
                    committed_trip = list(cur)
                    break
                # Try multiple drop strategies; commit to the first that works,
                # otherwise drop latest-deadline and continue shrinking.
                idx_lat = max(range(len(cur)), key=lambda i: cur[i]['deadline'])
                idx_hvy = max(range(len(cur)), key=lambda i: cur[i]['weight'])
                idx_far = max(range(len(cur)),
                              key=lambda i: dist(cur[i]['x'], cur[i]['y'], wx, wy))
                candidates = [idx_lat]
                if idx_hvy not in candidates:
                    candidates.append(idx_hvy)
                if idx_far not in candidates:
                    candidates.append(idx_far)

                for ci in candidates:
                    trial = cur[:ci] + cur[ci + 1:]
                    if not trial:
                        continue
                    r2, _o2 = try_trip(trial)
                    if r2 is not None:
                        result = r2
                        committed_trip = list(trial)
                        break
                if result is not None:
                    break
                cur.pop(idx_lat)

            if result is None:
                # No subset of the initial pack worked. The blocker is most
                # likely the earliest-deadline delivery — mark it as skipped
                # for THIS drone at THIS t_now and retry packing without it.
                # It remains unassigned so another drone can attempt it.
                skip_for_now.add(trip[0]['id'])
                continue

            path, end_t = result
            manifest.append({"drone_id": did, "path": path})
            for d in committed_trip:
                assigned.add(d['id'])
            t_now = end_t
            skip_for_now.clear()  # t_now changed — re-evaluate skipped items.

    return manifest
# End of BODY

# Start of TAIL
result = solve(warehouse, drones, deliveries, no_fly_zones, charging_stations)
output = {"flight_manifest": result}
print(json.dumps(output))
# End of TAIL

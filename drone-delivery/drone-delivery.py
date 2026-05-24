# Start of HEAD
import json
import sys
import math
from itertools import permutations

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
    BATTERY_CAP = 500.0
    CHARGE_RATE = 2.0
    EPS = 1e-7
    wx, wy = warehouse

    def dist(a, b):
        return math.hypot(a[0] - b[0], a[1] - b[1])

    # ---------- NFZ geometry ----------
    def pt_in_nfz_spatial(px, py, nfz):
        if nfz['shape'] == 'circle':
            cx, cy = nfz['center']
            r = nfz['radius']
            return (px - cx) ** 2 + (py - cy) ** 2 <= (r - EPS) ** 2
        else:
            (x1, y1), (x2, y2) = nfz['corners']
            return x1 + EPS <= px <= x2 - EPS and y1 + EPS <= py <= y2 - EPS

    def seg_spatial_window(ax, ay, bx, by, nfz):
        """Param interval s in [0,1] for which the segment lies inside the NFZ shape."""
        d = dist((ax, ay), (bx, by))
        if d < EPS:
            return (0.0, 1.0) if pt_in_nfz_spatial(ax, ay, nfz) else None
        dx, dy = bx - ax, by - ay
        if nfz['shape'] == 'circle':
            cx, cy = nfz['center']
            r = nfz['radius']
            ex, ey = ax - cx, ay - cy
            A = dx * dx + dy * dy
            B = 2 * (ex * dx + ey * dy)
            C = ex * ex + ey * ey - r * r
            disc = B * B - 4 * A * C
            if disc <= 0:
                return None
            sq = math.sqrt(disc)
            s1 = (-B - sq) / (2 * A)
            s2 = (-B + sq) / (2 * A)
            s_lo = max(0.0, s1)
            s_hi = min(1.0, s2)
            if s_lo >= s_hi:
                return None
            return (s_lo, s_hi)
        else:
            (x1, y1), (x2, y2) = nfz['corners']
            if abs(dx) > EPS:
                tx1, tx2 = (x1 - ax) / dx, (x2 - ax) / dx
                if tx1 > tx2:
                    tx1, tx2 = tx2, tx1
            else:
                if x1 <= ax <= x2:
                    tx1, tx2 = -math.inf, math.inf
                else:
                    return None
            if abs(dy) > EPS:
                ty1, ty2 = (y1 - ay) / dy, (y2 - ay) / dy
                if ty1 > ty2:
                    ty1, ty2 = ty2, ty1
            else:
                if y1 <= ay <= y2:
                    ty1, ty2 = -math.inf, math.inf
                else:
                    return None
            s_lo = max(0.0, tx1, ty1)
            s_hi = min(1.0, tx2, ty2)
            if s_lo >= s_hi:
                return None
            return (s_lo, s_hi)

    def seg_blocked_by(ax, ay, bx, by, t0, nfz):
        win = seg_spatial_window(ax, ay, bx, by, nfz)
        if win is None:
            return False
        d = dist((ax, ay), (bx, by))
        t_enter = t0 + win[0] * d
        t_leave = t0 + win[1] * d
        if t_leave <= nfz['T_start'] + EPS:
            return False
        if t_enter >= nfz['T_end'] - EPS:
            return False
        return True

    def blocked(ax, ay, bx, by, t0):
        for nfz in no_fly_zones:
            if seg_blocked_by(ax, ay, bx, by, t0, nfz):
                return True
        return False

    def wait_pos_safe(ax, ay, t0, t1):
        for nfz in no_fly_zones:
            if pt_in_nfz_spatial(ax, ay, nfz):
                if not (t1 <= nfz['T_start'] + EPS or t0 >= nfz['T_end'] - EPS):
                    return False
        return True

    def earliest_departure(ax, ay, bx, by, t0):
        if not blocked(ax, ay, bx, by, t0):
            return t0
        d = dist((ax, ay), (bx, by))
        cands = set()
        for nfz in no_fly_zones:
            win = seg_spatial_window(ax, ay, bx, by, nfz)
            if win is None:
                continue
            cands.add(nfz['T_end'] - win[0] * d + 1e-5)
        for td in sorted(cands):
            if td < t0 - EPS:
                continue
            if td < t0:
                td = t0
            if not wait_pos_safe(ax, ay, t0, td):
                continue
            if not blocked(ax, ay, bx, by, td):
                return td
        return None

    # ---------- Charging-station bookings ----------
    cs_bookings = [[] for _ in charging_stations]

    def cs_slot_available(ci, t_start, t_end):
        slots = charging_stations[ci].get('slots', 1) or 1
        overlap = 0
        for (s, e) in cs_bookings[ci]:
            if s < t_end - EPS and e > t_start + EPS:
                overlap += 1
        return overlap < slots

    # ---------- Trip simulation ----------
    def simulate_trip(order, trip_dels, t_start):
        path = []
        t = t_start
        bat = BATTERY_CAP
        pos = (wx, wy)
        w = sum(d['weight'] for d in trip_dels)

        for nfz in no_fly_zones:
            if pt_in_nfz_spatial(wx, wy, nfz) and nfz['T_start'] - EPS <= t <= nfz['T_end'] + EPS:
                return None

        path.append({
            "x": wx, "y": wy, "t": t,
            "action": "PICKUP",
            "delivery_ids": [trip_dels[i]['id'] for i in order],
        })

        for idx in order:
            d = trip_dels[idx]
            dp = (d['x'], d['y'])
            seg = dist(pos, dp)

            td = earliest_departure(pos[0], pos[1], dp[0], dp[1], t)
            if td is None:
                return None
            if td > t + EPS:
                t = td
                path.append({"x": pos[0], "y": pos[1], "t": t, "action": "WAIT"})

            energy = seg * (1 + w)
            if bat - energy < -EPS:
                return None
            bat -= energy
            t += seg
            if t > d['deadline'] + EPS:
                return None
            path.append({
                "x": dp[0], "y": dp[1], "t": t,
                "action": "DELIVER", "delivery_id": d['id'],
            })
            w -= d['weight']
            pos = dp

        ret_d = dist(pos, (wx, wy))
        if bat - ret_d >= -EPS:
            td = earliest_departure(pos[0], pos[1], wx, wy, t)
            if td is None:
                return None
            if td > t + EPS:
                t = td
                path.append({"x": pos[0], "y": pos[1], "t": t, "action": "WAIT"})
            bat -= ret_d
            t += ret_d
            path.append({"x": wx, "y": wy, "t": t, "action": "RETURN"})
            return path, t, []

        best = None
        for ci, cs in enumerate(charging_stations):
            cp = (cs['x'], cs['y'])
            d2cs = dist(pos, cp)
            if bat - d2cs < -EPS:
                continue
            td1 = earliest_departure(pos[0], pos[1], cp[0], cp[1], t)
            if td1 is None:
                continue
            t_cs_arr = td1 + d2cs
            bat_at_cs = bat - d2cs
            d_cw = dist(cp, (wx, wy))
            needed = max(0.0, d_cw - bat_at_cs)
            ct = math.ceil(needed / CHARGE_RATE)
            if not cs_slot_available(ci, t_cs_arr, t_cs_arr + ct):
                continue
            t_after_charge = t_cs_arr + ct
            td2 = earliest_departure(cp[0], cp[1], wx, wy, t_after_charge)
            if td2 is None:
                continue
            total_end = td2 + d_cw
            if best is None or total_end < best[0]:
                best = (total_end, ci, cp, td1, d2cs, ct, td2, d_cw)

        if best is None:
            return None
        total_end, ci, cp, td1, d2cs, ct, td2, d_cw = best

        if td1 > t + EPS:
            t = td1
            path.append({"x": pos[0], "y": pos[1], "t": t, "action": "WAIT"})
        bat -= d2cs
        t += d2cs
        path.append({"x": cp[0], "y": cp[1], "t": t, "action": "CHARGE"})
        t_cs_arr = t
        bat = min(BATTERY_CAP, bat + ct * CHARGE_RATE)
        t += ct
        path.append({"x": cp[0], "y": cp[1], "t": t, "action": "CHARGE_COMPLETE"})
        new_booking = (ci, t_cs_arr, t)

        if td2 > t + EPS:
            t = td2
            path.append({"x": cp[0], "y": cp[1], "t": t, "action": "WAIT"})
        bat -= d_cw
        t += d_cw
        path.append({"x": wx, "y": wy, "t": t, "action": "RETURN"})
        return path, t, [new_booking]

    def best_order_for_trip(trip_dels, t_start):
        n = len(trip_dels)
        best_result = None
        best_end = math.inf

        def try_order(order):
            nonlocal best_result, best_end
            res = simulate_trip(order, trip_dels, t_start)
            if res is None:
                return
            path, end_t, new_books = res
            if end_t < best_end:
                best_end = end_t
                best_result = (path, end_t, new_books)

        if n <= 7:
            for perm in permutations(range(n)):
                try_order(list(perm))
        else:
            remaining = list(range(n))
            order = []
            pos = (wx, wy)
            while remaining:
                remaining.sort(key=lambda i: (trip_dels[i]['deadline'],
                                              dist(pos, (trip_dels[i]['x'], trip_dels[i]['y']))))
                nxt = remaining.pop(0)
                order.append(nxt)
                pos = (trip_dels[nxt]['x'], trip_dels[nxt]['y'])
            try_order(order)
            order2 = sorted(range(n), key=lambda i: trip_dels[i]['deadline'])
            if order2 != order:
                try_order(order2)

        if best_result is None:
            return None
        path, end_t, new_books = best_result
        for (ci, s, e) in new_books:
            cs_bookings[ci].append((s, e))
        return path, end_t

    # ---------- Packing into trips ----------
    assigned = set()
    drone_t = {dr['id']: 0.0 for dr in drones}
    drone_paths = {dr['id']: [] for dr in drones}

    progress = True
    while progress and any(d['id'] not in assigned for d in deliveries):
        progress = False
        # Sort drones by current time to balance load
        sorted_drones = sorted(drones, key=lambda dr: drone_t[dr['id']])
        for dr in sorted_drones:
            cap = dr['max_payload']
            t_now = drone_t[dr['id']]
            pending = sorted(
                [d for d in deliveries if d['id'] not in assigned and d['weight'] <= cap + EPS],
                key=lambda d: d['deadline'],
            )
            if not pending:
                continue
            trip = []
            total_w = 0.0
            for d in pending:
                if len(trip) >= 7:
                    break
                if total_w + d['weight'] <= cap + EPS:
                    trip.append(d)
                    total_w += d['weight']
            if not trip:
                continue
            chosen = None
            attempt = list(trip)
            while attempt:
                res = best_order_for_trip(attempt, t_now)
                if res is not None:
                    chosen = (res, attempt)
                    break
                attempt.pop()
            if chosen is None:
                # Fallback: try each pending delivery alone (any may still be feasible)
                for d in pending:
                    res = best_order_for_trip([d], t_now)
                    if res is not None:
                        chosen = (res, [d])
                        break
            if chosen is None:
                continue
            (path, end_t), used = chosen
            drone_paths[dr['id']].extend(path)
            drone_t[dr['id']] = end_t
            for d in used:
                assigned.add(d['id'])
            progress = True

    manifest = []
    for dr in drones:
        p = drone_paths[dr['id']]
        if p:
            manifest.append({"drone_id": dr['id'], "path": p})

    return manifest
# End of BODY

# Start of TAIL
result = solve(warehouse, drones, deliveries, no_fly_zones, charging_stations)
output = {"flight_manifest": result}
print(json.dumps(output))
# End of TAIL

import numpy as np
import math
import queue as q
from collections import defaultdict

def segment_distance(segment1, segment2):
    if isinstance(segment1, tuple):
        segment1 = np.array(segment1)
    if isinstance(segment2, tuple):
        segment2 = np.array(segment2)

    if segment1.ndim == 1:
        segment1 = segment1.reshape((1, 2))
    if segment2.ndim == 1:
        segment2 = segment2.reshape((1, 2))

    # Handle single-point segments
    if segment1.shape[0] == 1:
        segment1 = np.repeat(segment1, 2, axis=0)
    if segment2.shape[0] == 1:
        segment2 = np.repeat(segment2, 2, axis=0)

    x1, y1 = segment1[0]
    x2, y2 = segment1[1]
    x3, y3 = segment2[0]
    x4, y4 = segment2[1]

    dx1 = x2 - x1
    dy1 = y2 - y1
    dx2 = x4 - x3
    dy2 = y4 - y3

    denominator = (-dy1 * dx2 + dx1 * dy2)

    t0_numerator = (x1 - x3) * dy2 - (y1 - y3) * dx2
    t1_numerator = (x1 - x3) * dy1 - (y1 - y3) * dx1

    if denominator == 0:
        # The segments are parallel.
        if t0_numerator == 0 and t1_numerator == 0:
            # The segments are coincident.
            return 0
        else:
            # The segments are not coincident.
            return min(np.linalg.norm(segment1 - segment2[0]), np.linalg.norm(segment1 - segment2[1]))

    t0 = t0_numerator / denominator
    t1 = t1_numerator / denominator

    if 0 <= t0 <= 1 and 0 <= t1 <= 1:
        # The intersection point lies within both segments.
        intersection = np.array([x1 + t0 * dx1, y1 + t0 * dy1])
        return 0
    else:
        # Find the closest endpoint.
        return min(np.linalg.norm(segment1 - segment2[0]), np.linalg.norm(segment1 - segment2[1]))
    
def N(segments, e, line):
    return [segment for segment in segments if segment_distance(segment, line) <= e]

def ExpandCluster(segments, classified_segments, Q, clusterId, e, minLns):
    while not Q.empty():
        M = Q.get()
        neighborhood = N(segments, e, M)

        if len(neighborhood) <= minLns:
            for neighbor in neighborhood:
                if classified_segments[str(neighbor)] is None or classified_segments[str(neighbor)] == -1:
                    classified_segments[str(neighbor)] = clusterId
                    if not np.array_equal(M, neighbor):  # Avoid adding the same segment again
                        Q.append(neighbor)

def LSC(segments, e = 0.1, minLns = 100):
    """Line Segment Clustering"""

    clusterId = 0
    classified_segments = {}

    # Convert segments to a list of tuples for better handling
    segments_list = [tuple(segment) for segment in segments]

    for seg in segments_list:
        classified_segments[str(seg)] = None

    for seg in segments_list:
        if classified_segments[str(seg)] is None:
            # Compute Nε(L);
            neighborhood = N(segments_list, e, seg)

            if len(neighborhood) >= minLns:
                Q = q.SimpleQueue()  # I assume 'q.SimpleQueue' is defined elsewhere

                for neighbor in neighborhood:
                    classified_segments[str(neighbor)] = clusterId
                    if not np.array_equal(seg, neighbor):
                        Q.put(neighbor)

                ###Step 2###
                ExpandCluster(segments_list, classified_segments, Q, clusterId, e, minLns)

                clusterId += 1
            else:
                classified_segments[str(seg)] = -1

    ###Step 3###
    o = defaultdict(list)
    for seg in segments_list:
        o[classified_segments[str(seg)]].append(seg)

    # Remove clusters with less than minLns elements
    o = {k: v for k, v in o.items() if len(v) >= minLns}
    if o == {}:
        return np.array([])    
    return np.array(o[0])

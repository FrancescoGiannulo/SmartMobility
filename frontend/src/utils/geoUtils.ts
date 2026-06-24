export function puntoInPoligono(
  lat: number,
  lng: number,
  perimetro: { type: 'Polygon'; coordinates: number[][][] }
): boolean {
  const ring = perimetro.coordinates[0]
  let inside = false
  for (let i = 0, j = ring.length - 1; i < ring.length; j = i++) {
    const xi = ring[i][0]; const yi = ring[i][1] // [lng, lat]
    const xj = ring[j][0]; const yj = ring[j][1]
    const intersect = yi > lat !== yj > lat &&
      lng < ((xj - xi) * (lat - yi)) / (yj - yi) + xi
    if (intersect) inside = !inside
  }
  return inside
}

export function distanzaDaPoligono(
  lat: number,
  lng: number,
  perimetro: { type: 'Polygon'; coordinates: number[][][] }
): number {
  const ring = perimetro.coordinates[0]
  const toRad = Math.PI / 180
  const mPerDegLat = 111_320
  const mPerDegLng = 111_320 * Math.cos(lat * toRad)

  const px = lng * mPerDegLng
  const py = lat * mPerDegLat

  let minDist = Infinity
  for (let i = 0, j = ring.length - 1; i < ring.length; j = i++) {
    const ax = ring[j][0] * mPerDegLng, ay = ring[j][1] * mPerDegLat
    const bx = ring[i][0] * mPerDegLng, by = ring[i][1] * mPerDegLat
    const dx = bx - ax, dy = by - ay
    const lenSq = dx * dx + dy * dy
    let t = lenSq > 0 ? ((px - ax) * dx + (py - ay) * dy) / lenSq : 0
    t = Math.max(0, Math.min(1, t))
    const cx = ax + t * dx, cy = ay + t * dy
    const ex = px - cx, ey = py - cy
    const dist = Math.sqrt(ex * ex + ey * ey)
    if (dist < minDist) minDist = dist
  }
  return minDist
}

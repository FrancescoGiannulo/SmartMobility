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

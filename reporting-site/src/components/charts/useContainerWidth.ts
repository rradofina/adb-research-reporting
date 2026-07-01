import { useEffect, useRef, useState } from "react";

/**
 * Measure a container's content width so charts can render their SVG at
 * 1:1 pixels (viewBox === pixel size). Rendering at 1:1 keeps SVG text at
 * real px sizes on every viewport — the single biggest legibility win
 * over a fixed-size raster that just scales down on mobile.
 */
export function useContainerWidth<T extends HTMLElement = HTMLDivElement>(): [
  React.RefObject<T | null>,
  number,
] {
  const ref = useRef<T>(null);
  const [width, setWidth] = useState(0);

  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    const update = () => setWidth(el.clientWidth);
    update();
    const ro = new ResizeObserver(update);
    ro.observe(el);
    return () => ro.disconnect();
  }, []);

  return [ref, width];
}

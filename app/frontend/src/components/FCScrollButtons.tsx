/**
 * @file FCScrollButtons.tsx
 *
 * The functional component for the scroll to top and scroll to bottom buttons,
 * used at the bottom of the chat input.
 */

import { IconButton, Tooltip } from "@radix-ui/themes";
import { RefObject, useEffect, useRef, useState } from "react";
import { GoMoveToBottom, GoMoveToTop } from "react-icons/go";
import { scrollToBottom, scrollToTop } from "../utils";

interface FCScrollButtonsProps {
  containerRef: RefObject<HTMLElement | null>;
}

export const FCScrollButtons = ({ containerRef }: FCScrollButtonsProps) => {
  const [canScrollUp, setCanScrollUp] = useState<boolean>(false);
  const [canScrollDown, setCanScrollDown] = useState<boolean>(false);
  const debounceTimer = useRef<number | null>(null);

  // Handler for the container scroll event; it is debounced for better
  // performance
  const handleScroll = () => {
    if (debounceTimer.current !== null) {
      clearTimeout(debounceTimer.current);
    }
    debounceTimer.current = setTimeout(() => {
      if (containerRef.current !== null) {
        const { scrollTop, scrollHeight, clientHeight } = containerRef.current;
        setCanScrollUp(scrollTop > 0);
        setCanScrollDown(scrollTop + clientHeight < scrollHeight);
      }
    }, 300);
  };

  useEffect(() => {
    const container = containerRef.current;
    if (container !== null) {
      container.addEventListener("scroll", handleScroll, { passive: true });
    }

    return () => {
      if (container !== null) {
        container.removeEventListener("scroll", handleScroll);
      }
      if (debounceTimer.current !== null) {
        clearTimeout(debounceTimer.current);
      }
    };
  }, [containerRef]);

  return (
    <>
      <Tooltip content="Scroll to top" side="top">
        <IconButton
          disabled={!canScrollUp}
          variant="ghost"
          size="1"
          onClick={() => scrollToTop(containerRef)}
        >
          <GoMoveToTop size="20" />
        </IconButton>
      </Tooltip>
      <Tooltip content="Scroll to bottom" side="top">
        <IconButton
          disabled={!canScrollDown}
          variant="ghost"
          size="1"
          onClick={() => scrollToBottom(containerRef)}
        >
          <GoMoveToBottom size="20" />
        </IconButton>
      </Tooltip>
    </>
  );
};

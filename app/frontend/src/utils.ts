/**
 * @file utils.ts
 *
 * This file contains utility functions that do not fit into any other category.
 */

import { RefObject } from "react";
import { UpdateMessagesFunction } from "./types";

/**
 * Get utility functions for adding user/bot messages.
 */
export const addMessageUtilities = (
  setMessages: (fn: UpdateMessagesFunction) => void,
) => {
  const addUserMessage = (element: React.ReactNode, text?: string) => {
    setMessages((prevMessages) => [
      ...prevMessages,
      { fromUser: true, element, text },
    ]);
  };

  const addBotMessage = (element: React.ReactNode, text?: string) => {
    setMessages((prevMessages) => [
      ...prevMessages,
      { fromUser: false, element, text },
    ]);
  };

  return { addUserMessage, addBotMessage };
};

/**
 * Scroll to the bottom of a React ref object.
 */
export const scrollToBottom = (ref: RefObject<HTMLElement>) => {
  if (ref.current !== null) {
    ref.current.scrollTo({
      top: ref.current.scrollHeight,
      behavior: "smooth",
    });
  }
};

/**
 * Scroll to the top of a React ref object.
 */
export const scrollToTop = (ref: RefObject<HTMLElement>) => {
  if (ref.current !== null) {
    ref.current.scrollTo({
      top: 0,
      behavior: "smooth",
    });
  }
};

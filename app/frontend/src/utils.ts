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
  const addUserMessage = (element: React.ReactNode) => {
    setMessages((prevMessages) => [
      ...prevMessages,
      { fromUser: true, element },
    ]);
  };

  const addBotMessage = (element: React.ReactNode) => {
    setMessages((prevMessages) => [
      ...prevMessages,
      { fromUser: false, element },
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

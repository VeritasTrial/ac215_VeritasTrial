/**
 * @file ChatInput.tsx
 *
 * The chat input box component.
 */

import { Box, Flex, TextArea } from "@radix-ui/themes";
import { Dispatch, ReactNode, SetStateAction, useRef } from "react";

interface ChatInputProps {
  query: string;
  setQuery: Dispatch<SetStateAction<string>>;
  onPressEnter: () => void;
  leftFunctionalComponents: ReactNode[];
  rightFunctionalComponents: ReactNode[];
}

export const ChatInput = ({
  query,
  setQuery,
  onPressEnter,
  leftFunctionalComponents,
  rightFunctionalComponents,
}: ChatInputProps) => {
  const textAreaRef = useRef<HTMLTextAreaElement>(null);

  return (
    <Box
      p="1"
      css={{
        borderRadius: "var(--radius-4)",
        backgroundColor: "var(--gray-4)",
        cursor: "text",
      }}
      onClick={() => {
        // Focus the text area when any part of the chat input area is clicked
        if (textAreaRef.current !== null) {
          textAreaRef.current.focus();
        }
      }}
    >
      <TextArea
        ref={textAreaRef}
        size="2"
        radius="large"
        css={{
          outline: "none",
          boxShadow: "none",
          backgroundColor: "transparent",
        }}
        placeholder="Enter your query here..."
        value={query}
        rows={4}
        onChange={(e) => setQuery(e.target.value)}
        onKeyDown={(e) => {
          if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            onPressEnter();
          }
        }}
      />
      <Flex justify="between" align="center" px="2" height="var(--space-7)">
        <Flex align="center" gap="2">
          {leftFunctionalComponents}
        </Flex>
        <Flex align="center" gap="2">
          {rightFunctionalComponents}
        </Flex>
      </Flex>
    </Box>
  );
};

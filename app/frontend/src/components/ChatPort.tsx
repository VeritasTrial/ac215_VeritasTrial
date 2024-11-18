/**
 * @file ChatPort.tsx
 *
 * The chat port component. This component is responsible for displaying a list
 * of chat messages that follows the chat display protocol.
 */

import { Avatar, Box, Flex, ScrollArea, Spinner, Text } from "@radix-ui/themes";
import { ChatDisplay } from "../types";
import { ForwardedRef, forwardRef } from "react";
import { FaUser } from "react-icons/fa";
import { RiRobot2Line } from "react-icons/ri";
import { CopyButton } from "./CopyButton";

interface ChatPortProps {
  messages: ChatDisplay[];
  loading: boolean;
}

export const ChatPort = forwardRef(
  ({ messages, loading }: ChatPortProps, ref: ForwardedRef<HTMLDivElement>) => {
    return (
      <ScrollArea
        ref={ref}
        scrollbars="vertical"
        css={{ "[data-radix-scroll-area-viewport] > div": { width: "100%" } }}
      >
        {/* List of chat messages, bots on left and user on right */}
        <Flex direction="column" justify="end" gap="3" pr="4" height="100%">
          {messages.map(({ fromUser, element, text }, index) => (
            <Flex
              key={index}
              direction={fromUser ? "row-reverse" : "row"}
              gap="3"
            >
              <Avatar
                size="2"
                fallback={fromUser ? <FaUser /> : <RiRobot2Line />}
              ></Avatar>
              <Box
                py="2"
                px="4"
                width="70%"
                overflowX="hidden"
                css={{
                  backgroundColor: fromUser
                    ? "var(--accent-4)"
                    : "var(--gray-surface)",
                  borderRadius: "var(--radius-3)",
                  whiteSpace: "pre-wrap",
                }}
              >
                {element}
              </Box>
              {text !== undefined && (
                <Box pt="2">
                  <CopyButton text={text} />
                </Box>
              )}
            </Flex>
          ))}
        </Flex>
        {/* Loading indicator */}
        <Flex
          align="center"
          justify="center"
          gap="3"
          pt="3"
          display={loading ? "flex" : "none"}
        >
          <Spinner loading={loading} />
          <Text size="2">Loading...</Text>
        </Flex>
      </ScrollArea>
    );
  },
);

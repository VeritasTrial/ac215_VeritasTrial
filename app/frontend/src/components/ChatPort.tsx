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
        <Flex direction="column" justify="end" gap="3" pr="4" height="100%">
          {messages.map(({ fromUser, element }) => (
            <Flex direction={fromUser ? "row-reverse" : "row"} gap="3">
              <Avatar
                size="2"
                fallback={fromUser ? <FaUser /> : <RiRobot2Line />}
              ></Avatar>
              <Box
                py="2"
                px="4"
                width="75%"
                overflowX="hidden"
                css={{
                  backgroundColor: fromUser
                    ? "var(--accent-3)"
                    : "var(--gray-4)",
                  borderRadius: "var(--radius-3)",
                }}
              >
                {element}
              </Box>
            </Flex>
          ))}
        </Flex>
        <Flex
          align="center"
          justify="center"
          gap="3"
          pt="3"
          display={loading ? "flex" : "none"}
        >
          <Spinner loading={loading} />
          <Text size="2">Retrieving results...</Text>
        </Flex>
      </ScrollArea>
    );
  },
);

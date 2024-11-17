/**
 * @file ChatErrorMessage.tsx
 *
 * The chat error message component. It should be displayed as a message from
 * the bot when an error occurs during the chat.
 */

import { Text } from "@radix-ui/themes";

interface ChatErrorMessageProps {
  error: string;
}

export const ChatErrorMessage = ({ error }: ChatErrorMessageProps) => {
  return (
    <Text
      size="2"
      as="div"
      color="red"
      css={{ whiteSpace: "pre", fontFamily: "var(--code-font-family)" }}
    >
      {error}
    </Text>
  );
};

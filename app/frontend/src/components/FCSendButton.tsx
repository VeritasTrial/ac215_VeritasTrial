/**
 * @file FCSendButton.tsx
 *
 * The functional component for the send button, used at the bottom of the chat
 * input.
 */

import { IconButton, Tooltip } from "@radix-ui/themes";
import { MdSend } from "react-icons/md";

interface FCSendButtonProps {
  disabled: boolean;
  onClick: () => void;
}

export const FCSendButton = ({ disabled, onClick }: FCSendButtonProps) => {
  return (
    <Tooltip content="Send" side="top">
      <IconButton
        disabled={disabled}
        variant="ghost"
        size="1"
        onClick={onClick}
      >
        <MdSend size="20" />
      </IconButton>
    </Tooltip>
  );
};

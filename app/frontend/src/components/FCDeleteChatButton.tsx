/**
 * @file FCDeleteChatButton.tsx
 *
 * The functional component for the delete chat button, used at the bottom of
 * the chat input.
 */

import { IconButton, Tooltip } from "@radix-ui/themes";
import { MdDeleteOutline } from "react-icons/md";

interface FCDeleteChatButtonProps {
  onClick: () => void;
}

export const FCDeleteChatButton = ({ onClick }: FCDeleteChatButtonProps) => {
  return (
    <Tooltip content="Delete chat" side="top">
      <IconButton variant="ghost" size="1" onClick={onClick} color="red">
        <MdDeleteOutline size="20" />
      </IconButton>
    </Tooltip>
  );
};

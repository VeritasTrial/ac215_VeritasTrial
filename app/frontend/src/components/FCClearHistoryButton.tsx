/**
 * @file FCClearHistoryButton.tsx
 *
 * The functional component for the clear history button, used at the bottom of
 * the chat input.
 */

import { IconButton, Tooltip } from "@radix-ui/themes";
import { MdClear } from "react-icons/md";

interface FCClearHistoryButtonProps {
  disabled: boolean;
  onClick: () => void;
}

export const FCClearHistoryButton = ({
  disabled,
  onClick,
}: FCClearHistoryButtonProps) => {
  return (
    <Tooltip content="Clear history" side="bottom">
      <IconButton
        disabled={disabled}
        variant="ghost"
        size="1"
        onClick={onClick}
      >
        <MdClear size="20" />
      </IconButton>
    </Tooltip>
  );
};

/**
 * @file CopyButton.tsx
 *
 * An icon button that copies the text content to the clipboard when clicked.
 */

import { IconButton, IconButtonProps } from "@radix-ui/themes";
import { MdContentCopy } from "react-icons/md";
import { toast } from "sonner";

type CopyButtonProps = IconButtonProps & {
  text: string;
};

export const CopyButton = ({ text, ...props }: CopyButtonProps) => {
  return (
    <IconButton
      size="1"
      variant="ghost"
      color="gray"
      onClick={async () => {
        await navigator.clipboard.writeText(text);
        toast.success("Copied to clipboard");
      }}
      {...props}
    >
      <MdContentCopy />
    </IconButton>
  );
};

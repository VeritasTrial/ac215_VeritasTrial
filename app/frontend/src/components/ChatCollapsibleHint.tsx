/**
 * @file ChatCollapsibleHint.tsx
 *
 * The collapsible hint component that should stay above the chat input area.
 */

import { Box, Flex, ScrollArea, Text } from "@radix-ui/themes";
import * as Collapsible from "@radix-ui/react-collapsible";
import { MdArrowDropDown } from "react-icons/md";
import { keyframes } from "@emotion/react";
import { PropsWithChildren, ReactNode } from "react";
import { IconType } from "react-icons";

const slideDown = keyframes({
  from: { height: 0 },
  to: { height: "var(--radix-collapsible-content-height)" },
});

const slideUp = keyframes({
  from: { height: "var(--radix-collapsible-content-height)" },
  to: { height: 0 },
});

type ChatCollapsibleHintProps = PropsWithChildren<{
  onToggleHint: () => void;
  hintText: string;
  HintIcon: IconType;
  rightHintComponent?: ReactNode;
}>;

export const ChatCollapsibleHint = ({
  onToggleHint,
  hintText,
  HintIcon,
  rightHintComponent,
  children,
}: ChatCollapsibleHintProps) => {
  return (
    <Collapsible.Root asChild>
      <Flex direction="column-reverse">
        <Collapsible.Trigger
          asChild
          onClick={() => {
            setTimeout(onToggleHint, 300);
          }}
          css={{
            '&[data-state="open"] > .chevron': {
              transform: "rotate(180deg)",
            },
          }}
        >
          <Flex
            width="100%"
            px="2"
            align="center"
            justify="between"
            css={{
              cursor: "pointer",
              backgroundColor: "var(--gray-4)",
              borderRadius: "var(--radius-3)",
            }}
          >
            <Flex align="center" gap="2" py="2">
              <HintIcon size="20" />
              <Text size="2">{hintText}</Text>
            </Flex>
            <Flex align="center" gap="2">
              {rightHintComponent}
              <MdArrowDropDown
                className="chevron"
                size="25"
                css={{ transition: "transform 300ms ease-in-out" }}
              />
            </Flex>
          </Flex>
        </Collapsible.Trigger>
        <Collapsible.Content
          css={{
            maxHeight: "20vh",
            '&[data-state="open"]': {
              animation: `${slideDown} 300ms ease-in-out`,
            },
            '&[data-state="closed"]': {
              animation: `${slideUp} 300ms ease-in-out`,
            },
          }}
        >
          <Box
            p="3"
            height="100%"
            css={{
              backgroundColor: "var(--gray-4)",
              borderTopLeftRadius: "var(--radius-3)",
              borderTopRightRadius: "var(--radius-3)",
              marginTop: "var(--radius-3)",
            }}
          >
            <ScrollArea scrollbars="vertical" asChild>
              <Box pr="2">{children}</Box>
            </ScrollArea>
          </Box>
        </Collapsible.Content>
      </Flex>
    </Collapsible.Root>
  );
};

/**
 * @file Sidebar.tsx
 *
 * The left-hand sidebar component.
 */

import { Box, Flex, RadioCards, ScrollArea, Text } from "@radix-ui/themes";
import { Dispatch, SetStateAction } from "react";
import { TbDatabaseSearch } from "react-icons/tb";
import { MetaInfo } from "../types";

interface SidebarProps {
  metaMapping: Map<string, MetaInfo>;
  currentTab: string;
  setCurrentTab: Dispatch<SetStateAction<string>>;
}

export const Sidebar = ({
  metaMapping,
  currentTab,
  setCurrentTab,
}: SidebarProps) => {
  return (
    <Flex direction="column" justify="between" height="100%">
      {/* Sidebar content */}
      <RadioCards.Root
        css={{ height: "80%", gridTemplateRows: "auto auto 1fr" }}
        size="1"
        variant="surface"
        columns="1"
        gap="0"
        value={currentTab}
        onValueChange={(value) => setCurrentTab(value)}
      >
        {/* Default retrieval tab */}
        <RadioCards.Item value="default">
          <Flex width="100%" gap="3" align="center">
            <TbDatabaseSearch size="30" />
            <Box>
              <Text size="2" as="div" weight="bold">
                Trial Retrieval
              </Text>
              <Text size="1" as="div">
                Search for trials to chat on
              </Text>
            </Box>
          </Flex>
        </RadioCards.Item>
        <Box pl="1" pt="4" pb="2">
          <Text size="2" weight="medium">
            Trials
          </Text>
        </Box>
        {/* List of chat tabs */}
        <ScrollArea scrollbars="vertical">
          <Flex direction="column" gap="2">
            {[...metaMapping].map(([tab, metaInfo]) => (
              <RadioCards.Item key={tab} value={tab}>
                <Text
                  size="2"
                  css={{
                    display: "-webkit-box",
                    textOverflow: "ellipsis",
                    WebkitLineClamp: 2,
                    WebkitBoxOrient: "vertical",
                    overflow: "hidden",
                  }}
                >
                  {metaInfo.title}
                </Text>
              </RadioCards.Item>
            ))}
          </Flex>
        </ScrollArea>
      </RadioCards.Root>
      {/* Sidebar footer */}
      <Box height="calc(20% - var(--space-3))" overflow="hidden">
        ABCDEFGHIJKLMNOPQRST ABCDEFGHIJKLMNOPQRST ABCDEFGHIJKLMNOPQRST
        ABCDEFGHIJKLMNOPQRST ABCDEFGHIJKLMNOPQRST ABCDEFGHIJKLMNOPQRST
      </Box>
    </Flex>
  );
};

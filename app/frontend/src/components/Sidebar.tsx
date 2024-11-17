/**
 * @file Sidebar.tsx
 *
 * The left-hand sidebar component.
 */

import {
  Box,
  Button,
  Flex,
  Link,
  RadioCards,
  ScrollArea,
  Text,
} from "@radix-ui/themes";
import { Dispatch, SetStateAction } from "react";
import { TbDatabaseSearch } from "react-icons/tb";
import { MetaInfo } from "../types";
import { MdDelete } from "react-icons/md";

interface SidebarProps {
  metaMapping: Map<string, MetaInfo>;
  currentTab: string;
  setCurrentTab: Dispatch<SetStateAction<string>>;
  clearTabs: () => void;
}

export const Sidebar = ({
  metaMapping,
  currentTab,
  setCurrentTab,
  clearTabs,
}: SidebarProps) => {
  return (
    <Flex direction="column" justify="between" height="100%">
      {/* Sidebar content */}
      <RadioCards.Root
        css={{ height: "85%", gridTemplateRows: "auto auto 1fr" }}
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
        {/* List of chat tabs */}
        {metaMapping.size > 0 && (
          <Box pl="1" pt="4" pb="2">
            <Text size="2" weight="medium">
              Chats
            </Text>
          </Box>
        )}
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
      <Flex
        height="calc(15% - var(--space-3))"
        direction="column"
        justify="end"
        gap="2"
        overflow="hidden"
      >
        <Button
          size="2"
          variant="surface"
          color="red"
          onClick={clearTabs}
          disabled={metaMapping.size === 0}
        >
          <MdDelete size="20" /> Delete all chats
        </Button>
        <Text size="1" color="gray" as="div" align="center">
          © 2024 <Link href="mailto:yaoxiao@g.harvard.edu">Yao Xiao</Link>,{" "}
          <Link href="mailto:bowenxu@g.harvard.edu">Bowen Xu</Link>,{" "}
          <Link href="mailto:tongxiao@g.harvard.edu">Tong Xiao</Link>
        </Text>
      </Flex>
    </Flex>
  );
};

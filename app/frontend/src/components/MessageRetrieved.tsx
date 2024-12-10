/**
 * @file MessageRetrieved.tsx
 *
 * This file contains the message component that displays the retrieved clinical
 * trials.
 */

import { Flex, IconButton, Text, Tooltip } from "@radix-ui/themes";
import { ExternalLink } from "./ExternalLink";
import { MdChat } from "react-icons/md";
import { CTGOV_URL } from "../consts";
import { MetaInfo } from "../types";
import { toast } from "sonner";

interface MessageRetrievedProps {
  ids: string[];
  titles: string[];
  switchTab: (tab: string, metaInfo: MetaInfo) => void;
}

export const MessageRetrieved = ({
  ids,
  titles,
  switchTab,
}: MessageRetrievedProps) => {
  return (
    <Flex direction="column" gap="3">
      <Text size="2" weight="medium">
        Here are the top {ids.length} clinical trials that match your query.
        Click the <MdChat css={{ verticalAlign: "middle" }} /> icon to start a
        chat on a specific trial.
      </Text>
      <Flex direction="column" gap="2">
        {ids.map((id, index) => (
          <Flex key={id} direction="column" gap="1">
            <Text size="2">{titles[index]}</Text>
            <Flex gap="2" align="center">
              <ExternalLink href={`${CTGOV_URL}/${id}`} size="2">
                {id}
              </ExternalLink>
              <Tooltip content="Start a chat" side="right">
                <IconButton
                  size="1"
                  variant="ghost"
                  onClick={() => {
                    switchTab(id, { title: titles[index] });
                    toast.success(`Chat started: ${id}`);
                  }}
                >
                  <MdChat />
                </IconButton>
              </Tooltip>
            </Flex>
          </Flex>
        ))}
      </Flex>
    </Flex>
  );
};

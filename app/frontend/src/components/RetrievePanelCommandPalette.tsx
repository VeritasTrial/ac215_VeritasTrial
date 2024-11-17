/**
 * @file RetrievalPanelCommandPalette.tsx
 *
 * The command palette component in the retrieval panel.
 */

import { Code, DataList, Flex, IconButton, Text } from "@radix-ui/themes";
import { MdContentCopy } from "react-icons/md";
import { ExternalLink } from "./ExternalLink";
import { PUBMED_URL } from "../consts";
import { MetaInfo } from "../types";

interface RetrievalPanelCommandPaletteProps {
  metaInfo: MetaInfo;
}

export const RetrievalPanelCommandPalette = ({
  metaInfo,
}: RetrievalPanelCommandPaletteProps) => {
  const { title } = metaInfo;

  return (
    <DataList.Root
      size="2"
      css={{ rowGap: "var(--space-2)", columnGap: "var(--space-6)" }}
    >
      {/* Full title */}
      <DataList.Item>
        <DataList.Label minWidth="0">
          <Flex align="center" gap="2">
            <Text>Full Title</Text>
            <IconButton
              size="1"
              variant="ghost"
              color="gray"
              onClick={() => navigator.clipboard.writeText(title)}
            >
              <MdContentCopy />
            </IconButton>
          </Flex>
        </DataList.Label>
        <DataList.Value>{title}</DataList.Value>
      </DataList.Item>
      {/* /meta command */}
      <DataList.Item>
        <DataList.Label minWidth="0">
          <Code>/meta</Code>
        </DataList.Label>
        <DataList.Value>Get metadata of the trial.</DataList.Value>
      </DataList.Item>
      {/* /docs command */}
      <DataList.Item>
        <DataList.Label minWidth="0">
          <Code>/docs</Code>
        </DataList.Label>
        <DataList.Value>
          <Text>
            Get references from{" "}
            <ExternalLink href={PUBMED_URL}>PubMed</ExternalLink> and other
            relevant documents.
          </Text>
        </DataList.Value>
      </DataList.Item>
    </DataList.Root>
  );
};

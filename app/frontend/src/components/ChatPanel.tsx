/**
 * @file ChatPanel.tsx
 *
 * The chat panel component in the body. In particular, this component is
 * responsible for taking user query, generating response with the specified
 * model and for the specified trial (by calling backend API), and displaying
 * the results.
 */

import { Code, DataList, Flex, IconButton, Text } from "@radix-ui/themes";
import { useEffect, useRef, useState } from "react";
import { MdContentCopy } from "react-icons/md";
import { GoCommandPalette } from "react-icons/go";
import { callChat } from "../api";
import {
  ChatDisplay,
  MetaInfo,
  ModelType,
  UpdateMessagesFunction,
} from "../types";
import { ChatPort } from "./ChatPort";
import { ChatInput } from "./ChatInput";
import { FCSendButton } from "./FCSendButton";
import { FCClearHistoryButton } from "./FCClearHistoryButton";
import { ExternalLink } from "./ExternalLink";
import { CTGOV_URL, PUBMED_URL } from "../consts";
import { ChatCollapsibleHint } from "./ChatCollapsibleHint";

interface ChatPanelProps {
  model: ModelType;
  tab: string;
  metaInfo: MetaInfo;
  messages: ChatDisplay[];
  setMessages: (fn: UpdateMessagesFunction) => void;
}

export const ChatPanel = ({
  model,
  tab,
  metaInfo,
  messages,
  setMessages,
}: ChatPanelProps) => {
  const chatPortRef = useRef<HTMLDivElement>(null);
  const [query, setQuery] = useState<string>("");
  const [loading, setLoading] = useState<boolean>(false);

  // Scroll the chat port to its bottom; this is so that the latest messages
  // are always visible
  const scrollChatPortToBottom = () => {
    if (chatPortRef.current !== null) {
      chatPortRef.current.scrollTo({
        top: chatPortRef.current.scrollHeight,
        behavior: "smooth",
      });
    }
  };

  // Handle the click event on the send button
  const handleSend = async () => {
    setLoading(true);

    // Clear the input area and add the user message to the list
    setQuery(""); // This will take effect only after the next render
    setMessages((prevMessages) => [
      ...prevMessages,
      { fromUser: true, element: <Text size="2">{query}</Text> },
    ]);

    // Call backend API to retrieve relevant clinical trials
    const callResult = await callChat(query, model, tab);
    if ("error" in callResult) {
      console.error(callResult.error);
    } else {
      const data = callResult.payload;
      setMessages((prevMessages) => [
        ...prevMessages,
        {
          fromUser: false,
          element: <Text size="2">{data.response}</Text>,
        },
      ]);
    }

    setLoading(false);
  };

  // Whenever there are new messages, scroll chat port to the bottom
  useEffect(() => {
    scrollChatPortToBottom();
  }, [messages]);

  return (
    <Flex direction="column" justify="end" gap="5" px="3" height="100%">
      <ChatPort ref={chatPortRef} messages={messages} loading={loading} />
      <Flex direction="column" gap="3">
        <ChatCollapsibleHint
          onToggleHint={scrollChatPortToBottom}
          hintText="Command palette"
          HintIcon={GoCommandPalette}
          rightHintComponent={
            <ExternalLink href={`${CTGOV_URL}/${tab}`} size="2">
              {tab}
            </ExternalLink>
          }
        >
          <DataList.Root
            size="2"
            css={{
              rowGap: "var(--space-2)",
              columnGap: "var(--space-6)",
            }}
          >
            <DataList.Item>
              <DataList.Label minWidth="0">
                <Flex align="center" gap="2">
                  <Text>Full Title</Text>
                  <IconButton
                    size="1"
                    variant="ghost"
                    color="gray"
                    onClick={() =>
                      navigator.clipboard.writeText(metaInfo.title)
                    }
                  >
                    <MdContentCopy />
                  </IconButton>
                </Flex>
              </DataList.Label>
              <DataList.Value>{metaInfo.title}</DataList.Value>
            </DataList.Item>
            <DataList.Item>
              <DataList.Label minWidth="0">
                <Code>/meta</Code>
              </DataList.Label>
              <DataList.Value>Get metadata of the trial.</DataList.Value>
            </DataList.Item>
            <DataList.Item>
              <DataList.Label minWidth="0">
                <Code>/docs</Code>
              </DataList.Label>
              <DataList.Value>
                <Text>
                  Get references from{" "}
                  <ExternalLink href={PUBMED_URL}>PubMed</ExternalLink> and
                  other relevant documents.
                </Text>
              </DataList.Value>
            </DataList.Item>
          </DataList.Root>
        </ChatCollapsibleHint>
        <ChatInput
          query={query}
          setQuery={setQuery}
          leftFunctionalComponents={
            <FCClearHistoryButton
              disabled={messages.length === 0 || loading}
              onClick={() => setMessages(() => [])}
            />
          }
          rightFunctionalComponents={
            <FCSendButton
              disabled={query === "" || loading}
              onClick={handleSend}
            />
          }
        />
      </Flex>
    </Flex>
  );
};

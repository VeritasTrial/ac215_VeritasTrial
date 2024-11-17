/**
 * @file ChatPanel.tsx
 *
 * The chat panel component in the body. In particular, this component is
 * responsible for taking user query, generating response with the specified
 * model and for the specified trial (by calling backend API), and displaying
 * the results.
 */

import {
  Box,
  Code,
  DataList,
  Flex,
  IconButton,
  Link,
  ScrollArea,
  Text,
  TextArea,
  Tooltip,
} from "@radix-ui/themes";
import { useEffect, useRef, useState } from "react";
import {
  MdArrowDropDown,
  MdClear,
  MdContentCopy,
  MdSend,
} from "react-icons/md";
import { GoCommandPalette } from "react-icons/go";
import { callChat } from "../api";
import * as Collapsible from "@radix-ui/react-collapsible";
import { keyframes } from "@emotion/react";
import {
  ChatDisplay,
  MetaInfo,
  ModelType,
  UpdateMessagesFunction,
} from "../types";
import { ChatPort } from "./ChatPort";

const slideDown = keyframes({
  from: { height: 0 },
  to: { height: "var(--radix-collapsible-content-height)" },
});

const slideUp = keyframes({
  from: { height: "var(--radix-collapsible-content-height)" },
  to: { height: 0 },
});

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
  const textAreaRef = useRef<HTMLTextAreaElement>(null);
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

  // Focus the text area; this is so that components other than the text area
  // itself can also focus the text area
  const focusTextArea = () => {
    if (textAreaRef.current !== null) {
      textAreaRef.current.focus();
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
        <Collapsible.Root asChild>
          <Flex direction="column-reverse">
            <Collapsible.Trigger
              asChild
              onClick={() =>
                // The timeout is to make sure that the collapsible animation is
                // completed before scrolling the chat port so the scroll height
                // can be calculated correctly
                setTimeout(scrollChatPortToBottom, 300)
              }
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
                  backgroundColor: "var(--gray-3)",
                  borderRadius: "var(--radius-3)",
                }}
              >
                <Flex align="center" gap="2" py="2">
                  <GoCommandPalette size="20" />
                  <Text size="2">Command palette</Text>
                </Flex>
                <Flex align="center" gap="2">
                  <Link
                    href={`https://clinicaltrials.gov/study/${tab}`}
                    target="_blank"
                    rel="noreferrer"
                    size="2"
                  >
                    {tab}
                  </Link>
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
                  backgroundColor: "var(--gray-3)",
                  borderTopLeftRadius: "var(--radius-3)",
                  borderTopRightRadius: "var(--radius-3)",
                  marginTop: "var(--radius-3)",
                }}
              >
                <ScrollArea scrollbars="vertical" asChild>
                  <Box pr="2">
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
                        <DataList.Value>
                          Get metadata of the trial.
                        </DataList.Value>
                      </DataList.Item>
                      <DataList.Item>
                        <DataList.Label minWidth="0">
                          <Code>/docs</Code>
                        </DataList.Label>
                        <DataList.Value>
                          <Text>
                            Get references from{" "}
                            <Link
                              href="https://pubmed.ncbi.nlm.nih.gov/"
                              target="_blank"
                              rel="noreferrer"
                            >
                              PubMed
                            </Link>{" "}
                            and other relevant documents.
                          </Text>
                        </DataList.Value>
                      </DataList.Item>
                    </DataList.Root>
                  </Box>
                </ScrollArea>
              </Box>
            </Collapsible.Content>
          </Flex>
        </Collapsible.Root>
        <Box
          p="1"
          css={{
            borderRadius: "var(--radius-4)",
            backgroundColor: "var(--gray-3)",
            cursor: "text",
          }}
          onClick={focusTextArea}
        >
          <TextArea
            ref={textAreaRef}
            size="2"
            radius="large"
            css={{
              outline: "none",
              boxShadow: "none",
              backgroundColor: "transparent",
            }}
            placeholder="Enter your query here..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            rows={5}
          />
          <Flex justify="between" align="center" px="2" height="var(--space-7)">
            <Tooltip content="Clear history" side="bottom">
              <IconButton
                disabled={messages.length === 0 || loading}
                variant="ghost"
                size="1"
                onClick={() => setMessages(() => [])}
              >
                <MdClear size="20" />
              </IconButton>
            </Tooltip>
            <Flex align="center" gap="3">
              <Tooltip content="Send" side="bottom">
                <IconButton
                  disabled={query === "" || loading}
                  variant="ghost"
                  size="1"
                  onClick={handleSend}
                >
                  <MdSend size="20" />
                </IconButton>
              </Tooltip>
            </Flex>
          </Flex>
        </Box>
      </Flex>
    </Flex>
  );
};

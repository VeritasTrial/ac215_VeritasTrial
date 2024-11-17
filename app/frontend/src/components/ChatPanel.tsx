/**
 * @file ChatPanel.tsx
 *
 * The chat panel component in the body. In particular, this component is
 * responsible for taking user query, generating response with the specified
 * model and for the specified trial (by calling backend API), and displaying
 * the results.
 */

import { Code, DataList, Flex, IconButton, Text } from "@radix-ui/themes";
import { ReactNode, useEffect, useRef, useState } from "react";
import { MdContentCopy } from "react-icons/md";
import { GoCommandPalette } from "react-icons/go";
import { callChat, callMeta } from "../api";
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
import { ChatErrorMessage } from "./ChatErrorMessage";

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
  const [extraRightFCs, setExtraRightFCs] = useState<ReactNode[]>([]);

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

    if (query === "/meta" || query === "/docs") {
      // Special commands where we only need to get metadata
      const callResult = await callMeta(tab);
      if ("error" in callResult) {
        setMessages((prevMessages) => [
          ...prevMessages,
          {
            fromUser: false,
            element: <ChatErrorMessage error={callResult.error} />,
          },
        ]);
      } else {
        const data = callResult.payload;
        if (query === "/meta") {
          setMessages((prevMessages) => [
            ...prevMessages,
            {
              fromUser: false,
              element: (
                <Text size="2">{JSON.stringify(data.metadata, null, 2)}</Text>
              ),
            },
          ]);
        } else {
          setMessages((prevMessages) => [
            ...prevMessages,
            {
              fromUser: false,
              element: (
                <Flex direction="column" gap="3">
                  {data.metadata.references.length > 0 ? (
                    <Flex direction="column" gap="1">
                      <Text size="2" weight="medium" mb="1">
                        References
                      </Text>
                      {data.metadata.references.map((ref) => (
                        <Flex align="center" justify="between" gap="2" pr="1">
                          <ExternalLink
                            key={ref.pmid}
                            href={`${PUBMED_URL}/${ref.pmid}`}
                            size="2"
                          >
                            {ref.citation}
                          </ExternalLink>{" "}
                          <IconButton
                            size="1"
                            variant="ghost"
                            color="gray"
                            onClick={() =>
                              navigator.clipboard.writeText(ref.citation)
                            }
                          >
                            <MdContentCopy />
                          </IconButton>
                        </Flex>
                      ))}
                    </Flex>
                  ) : (
                    <Text size="2" weight="medium" color="red">
                      No references found.
                    </Text>
                  )}
                  {data.metadata.documents.length > 0 ? (
                    <Flex direction="column" gap="1">
                      <Text size="2" weight="medium" mb="1">
                        Related Documents
                      </Text>
                      {data.metadata.documents.map((doc) => (
                        <Flex align="center" justify="between" gap="2" pr="1">
                          <ExternalLink key={doc.url} href={doc.url} size="2">
                            {doc.url.split("/").pop()}
                          </ExternalLink>{" "}
                          <Code variant="ghost" color="gray" size="2">
                            {Math.round(doc.size / 1024)}KB
                          </Code>
                        </Flex>
                      ))}
                    </Flex>
                  ) : (
                    <Text size="2" weight="medium" color="red">
                      No related documents found.
                    </Text>
                  )}
                </Flex>
              ),
            },
          ]);
        }
      }
    } else {
      // Normal chat command
      const callResult = await callChat(query, model, tab);
      if ("error" in callResult) {
        setMessages((prevMessages) => [
          ...prevMessages,
          {
            fromUser: false,
            element: <ChatErrorMessage error={callResult.error} />,
          },
        ]);
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
    }

    setLoading(false);
  };

  // Whenever there are new messages, scroll chat port to the bottom
  useEffect(() => {
    scrollChatPortToBottom();
  }, [messages]);

  // Extra right functional components based on the query
  useEffect(() => {
    const newFCs: ReactNode[] = [];
    if (query === "/meta") {
      newFCs.push(<Code size="2">/meta</Code>);
    } else if (query === "/docs") {
      newFCs.push(<Code size="2">/docs</Code>);
    }
    setExtraRightFCs(() => newFCs);
  }, [query]);

  const leftFCs = [
    <FCClearHistoryButton
      disabled={messages.length === 0 || loading}
      onClick={() => setMessages(() => [])}
    />,
  ];

  const rightFCs = [
    <FCSendButton disabled={query === "" || loading} onClick={handleSend} />,
  ];

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
          onPressEnter={async () => {
            if (query === "" || loading) {
              return;
            }
            await handleSend();
          }}
          leftFunctionalComponents={leftFCs}
          rightFunctionalComponents={[...extraRightFCs, rightFCs]}
        />
      </Flex>
    </Flex>
  );
};

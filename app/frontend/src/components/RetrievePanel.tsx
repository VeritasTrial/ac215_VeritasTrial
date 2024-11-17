/**
 * @file RetrievePanel.tsx
 *
 * The retrieval panel component in the body. In particular, this component is
 * responsible for taking user query, retrieving results from ChromaDB (by
 * calling backend API), and displaying the results.
 */

import { Flex, IconButton, Select, Text, Tooltip } from "@radix-ui/themes";
import { useEffect, useRef, useState } from "react";
import { MdChat, MdFilterList } from "react-icons/md";
import { callRetrieve } from "../api";
import { ChatDisplay, MetaInfo, UpdateMessagesFunction } from "../types";
import { ChatPort } from "./ChatPort";
import { ChatInput } from "./ChatInput";
import { FCSendButton } from "./FCSendButton";
import { FCClearHistoryButton } from "./FCClearHistoryButton";
import { ExternalLink } from "./ExternalLink";
import { CTGOV_URL } from "../consts";
import { ChatCollapsibleHint } from "./ChatCollapsibleHint";
import { ChatErrorMessage } from "./ChatErrorMessage";

interface RetrievalPanelProps {
  messages: ChatDisplay[];
  setMessages: (fn: UpdateMessagesFunction) => void;
  switchTab: (tab: string, metaInfo: MetaInfo) => void;
}

export const RetrievePanel = ({
  messages,
  setMessages,
  switchTab,
}: RetrievalPanelProps) => {
  const chatPortRef = useRef<HTMLDivElement>(null);
  const [query, setQuery] = useState<string>("");
  const [topK, setTopK] = useState<number>(3);
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
    const callResult = await callRetrieve(query, topK);
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
          element: (
            <Flex direction="column" gap="2">
              {data.ids.map((id, index) => (
                <Flex key={id} direction="column" gap="1">
                  <Text size="2">{data.documents[index]}</Text>
                  <Flex gap="2" align="center">
                    <ExternalLink href={`${CTGOV_URL}/${id}`} size="2">
                      {id}
                    </ExternalLink>
                    <Tooltip content="Start a chat" side="right">
                      <IconButton
                        size="1"
                        variant="ghost"
                        onClick={() =>
                          switchTab(id, { title: data.documents[index] })
                        }
                      >
                        <MdChat />
                      </IconButton>
                    </Tooltip>
                  </Flex>
                </Flex>
              ))}
            </Flex>
          ),
        },
      ]);
    }

    setLoading(false);
  };

  // Whenever there are new messages, scroll chat port to the bottom
  useEffect(() => {
    scrollChatPortToBottom();
  }, [messages]);

  const leftFunctionalComponents = [
    <FCClearHistoryButton
      disabled={messages.length === 0 || loading}
      onClick={() => setMessages(() => [])}
    />,
  ];

  const rightFunctionalComponents = [
    <Select.Root
      value={topK.toString()}
      onValueChange={(value: string) => setTopK(Number(value))}
      size="1"
    >
      <Select.Trigger variant="surface"></Select.Trigger>
      <Select.Content position="popper" sideOffset={5}>
        <Select.Item value="1">TopK: 1</Select.Item>
        <Select.Item value="3">TopK: 3</Select.Item>
        <Select.Item value="5">TopK: 5</Select.Item>
        <Select.Item value="10">TopK: 10</Select.Item>
        <Select.Item value="20">TopK: 20</Select.Item>
        <Select.Item value="30">TopK: 30</Select.Item>
      </Select.Content>
    </Select.Root>,
    <FCSendButton disabled={query === "" || loading} onClick={handleSend} />,
  ];

  return (
    <Flex direction="column" justify="end" gap="5" px="3" height="100%">
      <ChatPort ref={chatPortRef} messages={messages} loading={loading} />
      <Flex direction="column" gap="3">
        <ChatCollapsibleHint
          onToggleHint={scrollChatPortToBottom}
          hintText="Retrieval filters"
          HintIcon={MdFilterList}
        >
          TODO: FILTERS HERE!
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
          leftFunctionalComponents={leftFunctionalComponents}
          rightFunctionalComponents={rightFunctionalComponents}
        />
      </Flex>
    </Flex>
  );
};

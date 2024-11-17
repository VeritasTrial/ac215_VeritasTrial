/**
 * @file ChatPanel.tsx
 *
 * The chat panel component in the body. In particular, this component is
 * responsible for taking user query, generating response with the specified
 * model and for the specified trial (by calling backend API), and displaying
 * the results.
 */

import { Code, Flex, Text } from "@radix-ui/themes";
import { ReactNode, useEffect, useRef, useState } from "react";
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
import { CTGOV_URL } from "../consts";
import { ChatCollapsibleHint } from "./ChatCollapsibleHint";
import { ChatErrorMessage } from "./ChatErrorMessage";
import { addMessageUtilities, scrollToBottom } from "../utils";
import { MessageDocs } from "./MessageDocs";
import { RetrievalPanelCommandPalette } from "./RetrievePanelCommandPalette";

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
  const { addUserMessage, addBotMessage } = addMessageUtilities(setMessages);

  // Handle the click event on the send button
  const handleSend = async () => {
    setLoading(true);
    setQuery(""); // This will take effect only after the next render
    addUserMessage(<Text size="2">{query}</Text>);

    if (query === "/meta" || query === "/docs") {
      // Special commands where we only need to get metadata
      const callResult = await callMeta(tab);
      if ("error" in callResult) {
        addBotMessage(<ChatErrorMessage error={callResult.error} />);
      } else {
        const data = callResult.payload;
        if (query === "/meta") {
          addBotMessage(
            <Text size="2">{JSON.stringify(data.metadata, null, 2)}</Text>,
          );
        } else {
          addBotMessage(
            <MessageDocs
              references={data.metadata.references}
              documents={data.metadata.documents}
            />,
          );
        }
      }
    } else {
      // Normal chat command
      const callResult = await callChat(query, model, tab);
      if ("error" in callResult) {
        addBotMessage(<ChatErrorMessage error={callResult.error} />);
      } else {
        const data = callResult.payload;
        addBotMessage(<Text size="2">{data.response}</Text>);
      }
    }

    setLoading(false);
  };

  // Persistent left functional components
  const leftFCs = [
    <FCClearHistoryButton
      disabled={messages.length === 0 || loading}
      onClick={() => setMessages(() => [])}
    />,
  ];

  // Persistent right functional components
  const rightFCs = [
    <FCSendButton disabled={query === "" || loading} onClick={handleSend} />,
  ];

  // Whenever there are new messages, scroll chat port to the bottom
  useEffect(() => {
    scrollToBottom(chatPortRef);
  }, [messages]);

  // Update extra right functional components based on the query
  useEffect(() => {
    const newFCs: ReactNode[] = [];
    if (query === "/meta") {
      newFCs.push(<Code size="2">/meta</Code>);
    } else if (query === "/docs") {
      newFCs.push(<Code size="2">/docs</Code>);
    }
    setExtraRightFCs(() => newFCs);
  }, [query]);

  return (
    <Flex direction="column" justify="end" gap="5" px="3" height="100%">
      <ChatPort ref={chatPortRef} messages={messages} loading={loading} />
      <Flex direction="column" gap="3">
        <ChatCollapsibleHint
          onToggleHint={() => scrollToBottom(chatPortRef)}
          hintText="Command palette"
          HintIcon={GoCommandPalette}
          rightHintComponent={
            <ExternalLink href={`${CTGOV_URL}/${tab}`} size="2">
              {tab}
            </ExternalLink>
          }
        >
          <RetrievalPanelCommandPalette metaInfo={metaInfo} />
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

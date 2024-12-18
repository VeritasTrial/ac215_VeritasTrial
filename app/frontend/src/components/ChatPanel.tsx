/**
 * @file ChatPanel.tsx
 *
 * The chat panel component in the body. In particular, this component is
 * responsible for taking user query, generating response with the specified
 * model and for the specified trial (by calling backend API), and displaying
 * the results.
 */

import { Code, Flex, Text } from "@radix-ui/themes";
import {
  Dispatch,
  ReactNode,
  SetStateAction,
  useEffect,
  useRef,
  useState,
} from "react";
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
import { ChatPanelCommandPalette } from "./ChatPanelCommandPalette";
import { FCDeleteChatButton } from "./FCDeleteChatButton";
import { FCScrollButtons } from "./FCScrollButtons";
import { FCModelSelector } from "./FCModelSelector";
import { RadixMarkdown } from "./RadixMarkdown";
import { toast } from "sonner";

interface ChatPanelProps {
  tab: string;
  metaInfo: MetaInfo;
  model: ModelType;
  setModel: Dispatch<SetStateAction<ModelType>>;
  messages: ChatDisplay[];
  setMessages: (fn: UpdateMessagesFunction) => void;
  deleteTab: () => void;
}

export const ChatPanel = ({
  tab,
  metaInfo,
  model,
  setModel,
  messages,
  setMessages,
  deleteTab,
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
    addUserMessage(<RadixMarkdown text={query} />, query);

    if (query === "/meta" || query === "/docs") {
      // Special commands where we only need to get metadata
      const callResult = await callMeta(tab);
      if ("error" in callResult) {
        addBotMessage(
          <ChatErrorMessage error={callResult.error} />,
          callResult.error,
        );
      } else {
        const data = callResult.payload;
        if (query === "/meta") {
          addBotMessage(
            <Text size="2">{JSON.stringify(data.metadata, null, 2)}</Text>,
            JSON.stringify(data.metadata, null, 2),
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
        addBotMessage(
          <ChatErrorMessage error={callResult.error} />,
          callResult.error,
        );
      } else {
        const data = callResult.payload;
        addBotMessage(<RadixMarkdown text={data.response} />, data.response);
      }
    }

    setLoading(false);
  };

  // Persistent left functional components
  const leftFCs = [
    <FCClearHistoryButton
      key="clear-history-button"
      disabled={messages.length === 0 || loading}
      onClick={() => {
        setMessages(() => []);
        toast.success("Chat history cleared");
      }}
    />,
    <FCDeleteChatButton
      key="delete-chat-button"
      onClick={() => {
        deleteTab();
        toast.success(`Chat deleted: ${tab}`);
      }}
    />,
    <FCScrollButtons key="scroll-buttons" containerRef={chatPortRef} />,
  ];

  // Persistent right functional components
  const rightFCs = [
    <FCModelSelector key="model-selector" model={model} setModel={setModel} />,
    <FCSendButton
      key="send-button"
      disabled={query === "" || loading}
      onClick={handleSend}
    />,
  ];

  // Whenever there are new messages, scroll chat port to the bottom
  useEffect(() => {
    scrollToBottom(chatPortRef);
  }, [messages]);

  // Update extra right functional components based on the query
  useEffect(() => {
    const newFCs: ReactNode[] = [];
    if (query === "/meta") {
      newFCs.push(
        <Code key="hint-meta" size="2">
          /meta
        </Code>,
      );
    } else if (query === "/docs") {
      newFCs.push(
        <Code key="hint-docs" size="2">
          /docs
        </Code>,
      );
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
          <ChatPanelCommandPalette metaInfo={metaInfo} />
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

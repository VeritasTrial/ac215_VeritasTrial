/**
 * @file RetrievePanel.tsx
 *
 * The retrieval panel component in the body. In particular, this component is
 * responsible for taking user query, retrieving results from ChromaDB (by
 * calling backend API), and displaying the results.
 */

import { Button, Flex } from "@radix-ui/themes";
import { Dispatch, SetStateAction, useEffect, useRef, useState } from "react";
import { MdFilterList } from "react-icons/md";
import { callRetrieve } from "../api";
import {
  ChatDisplay,
  MetaInfo,
  TrialFilters,
  UpdateMessagesFunction,
} from "../types";
import { ChatPort } from "./ChatPort";
import { ChatInput } from "./ChatInput";
import { FCSendButton } from "./FCSendButton";
import { FCClearHistoryButton } from "./FCClearHistoryButton";
import { ChatCollapsibleHint } from "./ChatCollapsibleHint";
import { ChatErrorMessage } from "./ChatErrorMessage";
import { addMessageUtilities, scrollToBottom } from "../utils";
import { MessageRetrieved } from "./MessageRetrieved";
import { FCTopKSelector } from "./FCTopKSelector";
import { FCScrollButtons } from "./FCScrollButtons";
import { RadixMarkdown } from "./RadixMarkdown";
import { RetrievePanelFilters } from "./RetrievePanelFilters";
import { toast } from "sonner";

interface RetrievalPanelProps {
  messages: ChatDisplay[];
  setMessages: (fn: UpdateMessagesFunction) => void;
  filters: TrialFilters;
  setFilters: Dispatch<SetStateAction<TrialFilters>>;
  switchTab: (tab: string, metaInfo: MetaInfo) => void;
}

export const RetrievePanel = ({
  messages,
  setMessages,
  filters,
  setFilters,
  switchTab,
}: RetrievalPanelProps) => {
  const chatPortRef = useRef<HTMLDivElement>(null);
  const [query, setQuery] = useState<string>("");
  const [topK, setTopK] = useState<number>(3);
  const [loading, setLoading] = useState<boolean>(false);
  const { addUserMessage, addBotMessage } = addMessageUtilities(setMessages);

  // Handle the click event on the send button
  const handleSend = async () => {
    setLoading(true);
    setQuery(""); // This will take effect only after the next render
    addUserMessage(<RadixMarkdown text={query} />, query);

    const callResult = await callRetrieve(query, topK, filters);
    if ("error" in callResult) {
      addBotMessage(
        <ChatErrorMessage error={callResult.error} />,
        callResult.error,
      );
    } else {
      const data = callResult.payload;
      addBotMessage(
        <MessageRetrieved
          ids={data.ids}
          titles={data.documents}
          switchTab={switchTab}
        />,
      );
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
        toast.success("Retrieval history cleared");
      }}
    />,
    <FCScrollButtons key="scroll-buttons" containerRef={chatPortRef} />,
  ];

  // Persistent right functional components
  const rightFCs = [
    <FCTopKSelector
      key="top-k-selector"
      options={[1, 3, 5, 10, 20, 30]}
      value={topK}
      onValueChange={setTopK}
    />,
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

  return (
    <Flex direction="column" justify="end" gap="5" px="3" height="100%">
      <ChatPort ref={chatPortRef} messages={messages} loading={loading} />
      <Flex direction="column" gap="3">
        <ChatCollapsibleHint
          onToggleHint={() => scrollToBottom(chatPortRef)}
          hintText="Retrieval filters"
          HintIcon={MdFilterList}
          rightHintComponent={
            <Button
              size="1"
              variant="ghost"
              css={{ fontWeight: "var(--font-weight-medium)" }}
              onClick={(e) => {
                e.stopPropagation();
                setFilters({});
                toast.success("Retrieval filter reset");
              }}
            >
              Reset filters
            </Button>
          }
        >
          <RetrievePanelFilters filters={filters} setFilters={setFilters} />
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
          rightFunctionalComponents={rightFCs}
        />
      </Flex>
    </Flex>
  );
};

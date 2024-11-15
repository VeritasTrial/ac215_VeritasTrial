/**
 * @file RetrievePanel.tsx
 *
 * The retrieval panel component in the body. In particular, this component is
 * responsible for taking user query, retrieving results from ChromaDB (by
 * calling backend API), and displaying the results.
 */

import {
  Box,
  Flex,
  IconButton,
  ScrollArea,
  Select,
  Text,
  TextArea,
  Tooltip,
} from "@radix-ui/themes";
import { useEffect, useRef, useState } from "react";
import { MdArrowDropDown, MdFilterList, MdSend } from "react-icons/md";
import { callRetrieve } from "../api";
import * as Collapsible from "@radix-ui/react-collapsible";
import { keyframes } from "@emotion/react";
import { ChatDisplay } from "../types";

const slideDown = keyframes({
  from: { height: 0 },
  to: { height: "var(--radix-collapsible-content-height)" },
});

const slideUp = keyframes({
  from: { height: "var(--radix-collapsible-content-height)" },
  to: { height: 0 },
});

export const RetrievePanel = () => {
  const textAreaRef = useRef<HTMLTextAreaElement>(null);
  const chatPortRef = useRef<HTMLDivElement>(null);
  const [query, setQuery] = useState<string>("");
  const [topK, setTopK] = useState<number>(3);
  const [messages, setMessages] = useState<ChatDisplay[]>([]);

  // Whenever there are new messages, scroll to bottom of the viewport
  useEffect(() => {
    if (chatPortRef.current !== null) {
      chatPortRef.current.scrollTo({
        top: chatPortRef.current.scrollHeight,
        behavior: "smooth",
      });
    }
  }, [messages]);

  /**
   * Focus the text area.
   *
   * This is a helper function so that components other than the text area
   * itself can also focus the text area.
   */
  const focusTextArea = () => {
    if (textAreaRef.current !== null) {
      textAreaRef.current.focus();
    }
  };

  /**
   * Handle the send button click event.
   */
  const handleSend = async () => {
    // Add the user message to the list
    setMessages((prevMessages) => [
      ...prevMessages,
      { fromUser: true, element: query },
    ]);

    // Call backend API to retrieve relevant clinical trials
    const callResult = await callRetrieve(query, topK);
    if ("error" in callResult) {
      console.error(callResult.error);
      return;
    }
    const data = callResult.payload;
    setMessages((prevMessages) => [
      ...prevMessages,
      { fromUser: false, element: <pre>{JSON.stringify(data, null, 2)}</pre> },
    ]);
  };

  return (
    <Flex direction="column" justify="end" gap="3" px="3" height="100%">
      <ScrollArea ref={chatPortRef}>
        <Flex direction="column" justify="end" height="100%">
          {messages.map(({ fromUser, element }) =>
            fromUser ? (
              <Box>From user: {element}</Box>
            ) : (
              <Box>From bot: {element}</Box>
            ),
          )}
        </Flex>
      </ScrollArea>
      <Collapsible.Root asChild>
        <Flex direction="column-reverse">
          <Collapsible.Trigger
            asChild
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
                backgroundColor: "var(--gray-4)",
                borderRadius: "var(--radius-3)",
              }}
            >
              <Flex align="center" gap="2" py="2">
                <MdFilterList size="20" />
                <Text size="2">Refine your results with custom filters</Text>
              </Flex>
              <MdArrowDropDown
                className="chevron"
                size="25"
                css={{ transition: "transform 300ms ease-in-out" }}
              />
            </Flex>
          </Collapsible.Trigger>
          <Collapsible.Content
            css={{
              height: "20vh",
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
                backgroundColor: "var(--gray-4)",
                borderTopLeftRadius: "var(--radius-3)",
                borderTopRightRadius: "var(--radius-3)",
                marginTop: "var(--radius-3)",
              }}
            >
              <ScrollArea>TODO: FILTERS HERE!</ScrollArea>
            </Box>
          </Collapsible.Content>
        </Flex>
      </Collapsible.Root>
      <Box
        p="1"
        css={{
          borderRadius: "var(--radius-4)",
          backgroundColor: "var(--gray-4)",
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
        <Flex justify="end" align="center" gap="4" p="2">
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
          </Select.Root>
          <Tooltip content="Send" side="bottom">
            <IconButton
              disabled={query === ""}
              variant="ghost"
              size="1"
              onClick={handleSend}
            >
              <MdSend size="20" />
            </IconButton>
          </Tooltip>
        </Flex>
      </Box>
    </Flex>
  );
};

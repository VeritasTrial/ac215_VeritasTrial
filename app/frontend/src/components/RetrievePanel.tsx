/**
 * @file RetrievePanel.tsx
 *
 * The retrieval panel component in the body. In particular, this component is
 * responsible for taking user query, retrieving results from ChromaDB (by
 * calling backend API), and displaying the results.
 */

import { Box, Flex, IconButton, TextArea, Tooltip } from "@radix-ui/themes";
import { useRef, useState } from "react";
import { MdSend } from "react-icons/md";
import { callRetrieve } from "../api";

export const RetrievePanel = () => {
  const textAreaRef = useRef<HTMLTextAreaElement>(null);
  const [query, setQuery] = useState<string>("");
  const [response, setResponse] = useState<string>("");

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
   *
   * This function sends the query to the backend API and sets the response.
   */
  const handleSend = async () => {
    const callResult = await callRetrieve(query);
    if ("error" in callResult) {
      setResponse(callResult.error);
      return;
    }
    const data = callResult.payload;
    setResponse(JSON.stringify(data, null, 2));
  };

  return (
    <Flex direction="column" gap="3" px="3">
      <Box>{response}</Box>
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
        <Flex justify="end" p="2">
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

/**
 * @file RetrievePanel.tsx
 *
 * The retrieval panel component in the body. In particular, this component is
 * responsible for taking user query, retrieving results from ChromaDB (by
 * calling backend API), and displaying the results.
 */

import { Box, Button, Flex, TextArea } from "@radix-ui/themes";
import { useState } from "react";
import { callRetrieve } from "../api";

export const RetrievePanel = () => {
  const [query, setQuery] = useState<string>("");
  const [response, setResponse] = useState<string>("");

  const handleSubmit = async () => {
    const callResult = await callRetrieve(query);
    if ("error" in callResult) {
      setResponse(callResult.error);
      return;
    }
    const data = callResult.payload;
    setResponse(JSON.stringify(data, null, 2));
  };

  return (
    <Flex direction="column" gap="3">
      <Box>{response}</Box>
      <Box>
        <TextArea
          placeholder="Enter your query here..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          rows={5}
        />
      </Box>
      <Box>
        <Button variant="solid" color="indigo" size="2" onClick={handleSubmit}>
          Submit
        </Button>
      </Box>
    </Flex>
  );
};

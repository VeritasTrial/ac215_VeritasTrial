import {
  Box,
  Button,
  Flex,
  ScrollArea,
  Text,
  TextArea,
  Theme,
} from "@radix-ui/themes";
import { useState } from "react";
import queryString from "query-string";

export const App = () => {
  const [query, setQuery] = useState("");
  const [response, setResponse] = useState("");

  const handleSubmit = async () => {
    const params = queryString.stringify({ query });
    try {
      const res = await fetch(
        `${import.meta.env.VITE_BACKEND_URL}/generate?${params}`,
        {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
          },
        },
      );
      const data = await res.json();
      setResponse(data.response);
    } catch (e: unknown) {
      setResponse(`${e}`);
    }
  };

  return (
    <Theme appearance="dark" accentColor="indigo" grayColor="slate">
      <Flex
        align="center"
        justify="center"
        direction="column"
        gap="6"
        css={{ height: "100vh", backgroundColor: "var(--gray-1)" }}
      >
        <ScrollArea
          type="auto"
          css={{
            width: "60vw",
            height: "30vh",
            backgroundColor: "var(--gray-2)",
            borderRadius: "var(--radius-2)",
          }}
        >
          <Box py="3" px="5">
            <Text size="2" css={{ whiteSpace: "pre-wrap" }}>
              {response}
            </Text>
          </Box>
        </ScrollArea>
        <Flex
          align="center"
          justify="center"
          direction="column"
          gap="3"
          width="100%"
        >
          <TextArea
            placeholder="Type your query here..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            css={{ width: "40vw", height: "20vh" }}
          ></TextArea>
          <Button variant="outline" onClick={handleSubmit}>
            Submit
          </Button>
        </Flex>
      </Flex>
    </Theme>
  );
};

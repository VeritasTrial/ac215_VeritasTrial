import { Box, Button, Flex, TextArea, Theme } from "@radix-ui/themes";
import { useState } from "react";

export const App = () => {
  const [query, setQuery] = useState("");
  const [response, setResponse] = useState("ajdfkljadlkfs");

  return (
    <Theme appearance="dark" accentColor="indigo" grayColor="slate">
      <Flex align="center" justify="center" direction="column" gap="3" css={{ height: "100vh", backgroundColor: "var(--gray-1)" }}>
        <Box p="3">{response}</Box>
        <TextArea size="3" placeholder="Type your query here..." value={query} onChange={(e) => setQuery(e.target.value)} css={{ width: "40%", height: "20%" }}></TextArea>
        <Button size="2" variant="outline">Submit</Button>
      </Flex>
    </Theme>
  );
};

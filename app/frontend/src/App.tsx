/**
 * @file App.tsx
 *
 * The overall application.
 */

import { Box, Flex, Theme } from "@radix-ui/themes";
import { useState } from "react";
import { ApperanceType, ModelType } from "./types";
import { Header } from "./components/Header";
import { Sidebar } from "./components/Sidebar";
import { RetrievePanel } from "./components/RetrievePanel";

export const App = () => {
  const [appearance, setAppearance] = useState<ApperanceType>("dark");
  const [model, setModel] = useState<ModelType>("6894888983713546240");

  return (
    <Theme appearance={appearance} accentColor="indigo" grayColor="slate">
      <Flex css={{ height: "100vh" }}>
        <Box
          height="100%"
          width="20%"
          p="4"
          css={{ backgroundColor: "var(--gray-3)" }}
        >
          <Sidebar></Sidebar>
        </Box>
        <Flex
          height="100%"
          width="80%"
          direction="column"
          p="4"
          pl="6"
          css={{ backgroundColor: "var(--gray-1)" }}
        >
          <Box height="50px">
            <Header
              appearance={appearance}
              setAppearance={setAppearance}
              model={model}
              setModel={setModel}
            ></Header>
          </Box>
          <Box height="calc(100% - 50px)">
            <RetrievePanel></RetrievePanel>
          </Box>
        </Flex>
      </Flex>
    </Theme>
  );
};

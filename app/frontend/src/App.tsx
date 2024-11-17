/**
 * @file App.tsx
 *
 * The overall application.
 */

import { Box, Flex, Theme } from "@radix-ui/themes";
import { useState } from "react";
import {
  ApperanceType,
  ChatDisplay,
  MetaInfo,
  ModelType,
  UpdateMessagesFunction,
} from "./types";
import { Header } from "./components/Header";
import { Sidebar } from "./components/Sidebar";
import { RetrievePanel } from "./components/RetrievePanel";
import { ChatPanel } from "./components/ChatPanel";

export const App = () => {
  const [appearance, setAppearance] = useState<ApperanceType>("dark");
  const [model, setModel] = useState<ModelType>("6894888983713546240");
  const [currentTab, setCurrentTab] = useState<string>("default");
  const [messagesMapping, setMessagesMapping] = useState<
    Map<string, ChatDisplay[]>
  >(new Map([["default", []]]));
  const [metaMapping, setMetaMapping] = useState<Map<string, MetaInfo>>(
    new Map(),
  );

  // Switch to a different tab, creating a new tab if it does not exist yet
  const switchTab = (tab: string, metaInfo: MetaInfo) => {
    setMessagesMapping((prevMessagesMapping) => {
      const newMessagesMapping = new Map(prevMessagesMapping);
      if (!prevMessagesMapping.has(tab)) {
        newMessagesMapping.set(tab, []);
      }
      return newMessagesMapping;
    });
    setMetaMapping((prevMetaMapping) => {
      const newMetaMapping = new Map(prevMetaMapping);
      if (!prevMetaMapping.has(tab)) {
        newMetaMapping.set(tab, metaInfo);
      }
      return newMetaMapping;
    });
    setCurrentTab(tab);
  };

  return (
    <Theme appearance={appearance} accentColor="indigo" grayColor="slate">
      <Flex css={{ height: "100vh" }}>
        <Box
          height="100%"
          width="20%"
          p="4"
          css={{ backgroundColor: "var(--gray-3)" }}
        >
          <Sidebar
            metaMapping={metaMapping}
            currentTab={currentTab}
            setCurrentTab={setCurrentTab}
          ></Sidebar>
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
            {currentTab === "default" && (
              <RetrievePanel
                messages={messagesMapping.get("default")!}
                setMessages={(fn: UpdateMessagesFunction) =>
                  setMessagesMapping((prevMessagesMapping) => {
                    const newMessagesMapping = new Map(prevMessagesMapping);
                    newMessagesMapping.set(
                      "default",
                      fn(prevMessagesMapping.get("default")!),
                    );
                    return newMessagesMapping;
                  })
                }
                switchTab={switchTab}
              ></RetrievePanel>
            )}
            {currentTab !== "default" && (
              <ChatPanel
                model={model}
                tab={currentTab}
                metaInfo={metaMapping.get(currentTab)!}
                messages={messagesMapping.get(currentTab)!}
                setMessages={(fn: UpdateMessagesFunction) =>
                  setMessagesMapping((prevMessagesMapping) => {
                    const newMessagesMapping = new Map(prevMessagesMapping);
                    newMessagesMapping.set(
                      currentTab,
                      fn(prevMessagesMapping.get(currentTab)!),
                    );
                    return newMessagesMapping;
                  })
                }
              ></ChatPanel>
            )}
          </Box>
        </Flex>
      </Flex>
    </Theme>
  );
};

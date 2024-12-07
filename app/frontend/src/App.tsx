/**
 * @file App.tsx
 *
 * The overall application.
 */

import { Box, Flex, Theme } from "@radix-ui/themes";
import { useEffect, useRef, useState } from "react";
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
import { Toaster } from "sonner";

export const App = () => {
  const isDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
  const [appearance, setAppearance] = useState<ApperanceType>(
    isDark ? "dark" : "light",
  );
  const [model, setModel] = useState<ModelType>("6894888983713546240");
  const [currentTab, setCurrentTab] = useState<string>("default");
  const [messagesMapping, setMessagesMapping] = useState<
    Map<string, ChatDisplay[]>
  >(new Map([["default", []]]));
  const [metaMapping, setMetaMapping] = useState<Map<string, MetaInfo>>(
    new Map(),
  );
  const tabRefs = useRef<Map<string, HTMLButtonElement>>(new Map());

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

  // Delete a tab
  const deleteTab = (tab: string) => {
    setMessagesMapping((prevMessagesMapping) => {
      const newMessagesMapping = new Map(prevMessagesMapping);
      newMessagesMapping.delete(tab);
      return newMessagesMapping;
    });
    setMetaMapping((prevMetaMapping) => {
      const newMetaMapping = new Map(prevMetaMapping);
      newMetaMapping.delete(tab);
      return newMetaMapping;
    });
    setCurrentTab("default");
    tabRefs.current.delete(tab);
  };

  // Clear all tabs
  const clearTabs = () => {
    setMessagesMapping((prevMessagesMapping) => {
      const newMessagesMapping = new Map();
      newMessagesMapping.set("default", prevMessagesMapping.get("default")!);
      return newMessagesMapping;
    });
    setMetaMapping(new Map());
    setCurrentTab("default");
    tabRefs.current.clear();
  };

  // When the current tab changes, scroll to make it visible; note that the
  // "default" tab is not in the scroll area and is always visible
  useEffect(() => {
    if (currentTab !== "default" && tabRefs.current.has(currentTab)) {
      tabRefs.current.get(currentTab)!.scrollIntoView({
        behavior: "smooth",
        block: "nearest",
      });
    }
  }, [currentTab]);

  return (
    <Theme appearance={appearance} accentColor="indigo" grayColor="slate">
      <Toaster
        position="top-right"
        theme={appearance}
        gap={6}
        offset="var(--space-3)"
        toastOptions={{
          style: {
            color: "var(--gray-12)",
            borderColor: "var(--gray-6)",
            backgroundColor: "var(--gray-surface)",
            padding: "var(--space-2) var(--space-4)",
          },
        }}
      />
      <Flex css={{ height: "100vh" }}>
        {/* Left-hand sidebar panel */}
        <Box
          height="100%"
          width="20%"
          p="4"
          css={{ backgroundColor: "var(--gray-4)" }}
        >
          <Sidebar
            tabRefs={tabRefs}
            metaMapping={metaMapping}
            currentTab={currentTab}
            setCurrentTab={setCurrentTab}
            clearTabs={clearTabs}
          ></Sidebar>
        </Box>
        {/* Right-hand main panel */}
        <Flex
          height="100%"
          width="80%"
          direction="column"
          p="4"
          pl="6"
          css={{ backgroundColor: "var(--gray-1)" }}
        >
          {/* Top header */}
          <Box height="50px">
            <Header
              appearance={appearance}
              setAppearance={setAppearance}
            ></Header>
          </Box>
          {/* Main body */}
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
                tab={currentTab}
                metaInfo={metaMapping.get(currentTab)!}
                model={model}
                setModel={setModel}
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
                deleteTab={() => deleteTab(currentTab)}
              ></ChatPanel>
            )}
          </Box>
        </Flex>
      </Flex>
    </Theme>
  );
};

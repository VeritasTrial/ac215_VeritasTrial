/**
 * @file Header.tsx
 *
 * The header component in the body.
 */

import { Box, Flex, Heading, IconButton, Tooltip } from "@radix-ui/themes";
import { Dispatch, SetStateAction } from "react";
import { MdDarkMode, MdLightMode, MdMenu, MdMenuOpen } from "react-icons/md";
import { FaGithub, FaUniversity } from "react-icons/fa";
import { ApperanceType } from "../types";
import { AC215_URL, GITHUB_URL } from "../consts";
import { ExternalLink } from "./ExternalLink";

interface HeaderProps {
  appearance: ApperanceType;
  setAppearance: Dispatch<SetStateAction<ApperanceType>>;
  isSidebarVisible: boolean;
  isSidebarPopoverVisible: boolean;
  setIsSidebarPopoverVisible: Dispatch<SetStateAction<boolean>>;
}

export const Header = ({
  appearance,
  setAppearance,
  isSidebarVisible,
  isSidebarPopoverVisible,
  setIsSidebarPopoverVisible,
}: HeaderProps) => {
  const switchAppearance = () => {
    if (appearance === "dark") {
      setAppearance("light");
    } else {
      setAppearance("dark");
    }
  };

  return (
    <Flex justify="between" align="center" pr="3">
      <Box ml="2">
        <Heading size="4">VeritasTrial</Heading>
      </Box>
      <Flex align="center" gap="4">
        {!isSidebarVisible && (
          <Tooltip content="Toggle sidebar">
            <Box>
              <IconButton
                size="1"
                variant="ghost"
                onClick={() =>
                  setIsSidebarPopoverVisible(!isSidebarPopoverVisible)
                }
              >
                {isSidebarPopoverVisible ? (
                  <MdMenuOpen size="20" />
                ) : (
                  <MdMenu size="20" />
                )}
              </IconButton>
            </Box>
          </Tooltip>
        )}
        <Tooltip content="Harvard AC215">
          <Box>
            <IconButton size="1" variant="ghost" asChild>
              <ExternalLink href={AC215_URL}>
                <FaUniversity size="20" />
              </ExternalLink>
            </IconButton>
          </Box>
        </Tooltip>
        <Tooltip content="Source">
          <Box>
            <IconButton size="1" variant="ghost" asChild>
              <ExternalLink href={GITHUB_URL}>
                <FaGithub size="20" />
              </ExternalLink>
            </IconButton>
          </Box>
        </Tooltip>
        <Tooltip content="Toggle theme">
          <Box>
            <IconButton size="1" variant="ghost" onClick={switchAppearance}>
              {appearance === "dark" ? (
                <MdDarkMode size="20" />
              ) : (
                <MdLightMode size="20" />
              )}
            </IconButton>
          </Box>
        </Tooltip>
      </Flex>
    </Flex>
  );
};

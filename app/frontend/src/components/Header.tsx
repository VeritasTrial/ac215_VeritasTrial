/**
 * @file Header.tsx
 *
 * The header component in the body.
 */

import {
  Avatar,
  Box,
  Flex,
  IconButton,
  Select,
  Tooltip,
} from "@radix-ui/themes";
import { Dispatch, SetStateAction } from "react";
import { MdDarkMode, MdLightMode } from "react-icons/md";
import { FaGithub, FaUniversity } from "react-icons/fa";
import { ApperanceType, ModelType } from "../types";
import VeritasTrialLogo from "/veritastrial.svg";
import { AC215_URL, GITHUB_URL } from "../consts";
import { ExternalLink } from "./ExternalLink";

interface HeaderProps {
  appearance: ApperanceType;
  setAppearance: Dispatch<SetStateAction<ApperanceType>>;
  model: ModelType;
  setModel: Dispatch<SetStateAction<ModelType>>;
}

export const Header = ({
  appearance,
  setAppearance,
  model,
  setModel,
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
      {/* Left-aligned part of header */}
      <Flex align="center" gap="4">
        <Avatar src={VeritasTrialLogo} fallback="VT" size="2" />
        <Select.Root
          value={model}
          onValueChange={(value: ModelType) => setModel(value)}
          size="2"
        >
          <Select.Trigger variant="surface"></Select.Trigger>
          <Select.Content position="popper" sideOffset={5}>
            <Select.Item value="6894888983713546240">VeritasTrial</Select.Item>
            <Select.Item value="gemini-1.5-flash-001">
              Gemini 1.5 Flash
            </Select.Item>
          </Select.Content>
        </Select.Root>
      </Flex>
      {/* Right-aligned part of header */}
      <Flex align="center" gap="4">
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

/**
 * @file FCModelSelector.tsx
 *
 * The functional component for the chat model selector, used at the bottom of
 * the chat input.
 */

import { Select } from "@radix-ui/themes";
import { ModelType } from "../types";
import { Dispatch, SetStateAction } from "react";

interface FCModelSelectorProps {
  model: ModelType;
  setModel: Dispatch<SetStateAction<ModelType>>;
}

export const FCModelSelector = ({ model, setModel }: FCModelSelectorProps) => {
  return (
    <Select.Root
      value={model}
      onValueChange={(value: ModelType) => setModel(value)}
      size="1"
    >
      <Select.Trigger
        variant="surface"
        css={{ margin: "0 var(--space-1)" }}
      ></Select.Trigger>
      <Select.Content position="popper" sideOffset={5}>
        <Select.Item key="6894888983713546240" value="6894888983713546240">
          VeritasTrial
        </Select.Item>
        <Select.Item key="gemini-1.5-flash-001" value="gemini-1.5-flash-001">
          Gemini 1.5 Flash
        </Select.Item>
      </Select.Content>
    </Select.Root>
  );
};

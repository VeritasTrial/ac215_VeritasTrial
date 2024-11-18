/**
 * @file FCTopKSelector.tsx
 */

import { Select } from "@radix-ui/themes";

interface FCTopKSelectorProps {
  options: number[];
  value: number;
  onValueChange: (value: number) => void;
}

export const FCTopKSelector = ({
  options,
  value,
  onValueChange,
}: FCTopKSelectorProps) => {
  return (
    <Select.Root
      value={value.toString()}
      onValueChange={(value: string) => onValueChange(Number(value))}
      size="1"
    >
      <Select.Trigger
        variant="surface"
        css={{ margin: "0 var(--space-1)" }}
      ></Select.Trigger>
      <Select.Content position="popper" sideOffset={5}>
        {options.map((option) => (
          <Select.Item key={option} value={option.toString()}>
            TopK: {option}
          </Select.Item>
        ))}
      </Select.Content>
    </Select.Root>
  );
};

/**
 * @file RadixCalendar.tsx
 *
 * Customized calendar component based on react-day-picker.
 */

import { Select } from "@radix-ui/themes";
import { ChangeEvent } from "react";
import { DayPicker, DayPickerProps } from "react-day-picker";
import {
  IoChevronBack,
  IoChevronDown,
  IoChevronForward,
  IoChevronUp,
} from "react-icons/io5";

export const RadixCalendar = (props: DayPickerProps) => {
  return (
    <DayPicker
      styles={{
        month_caption: {
          justifyContent: "center",
          fontSize: "var(--font-size-2)",
          fontWeight: "var(--font-weight-medium)",
        },
        day: { fontSize: "var(--font-size-2)" },
        nav: { justifyContent: "space-between", width: "100%" },
      }}
      components={{
        Chevron: ({ ...props }) => {
          switch (props.orientation) {
            case "left":
              return <IoChevronBack />;
            case "right":
              return <IoChevronForward />;
            case "up":
              return <IoChevronUp />;
            case "down":
              return <IoChevronDown />;
            default:
              return <></>;
          }
        },
        Dropdown: ({ ...props }) => (
          <Select.Root
            size="1"
            value={props.value?.toString()}
            onValueChange={(value) => {
              if (props.onChange !== undefined) {
                props.onChange({
                  target: { value },
                } as ChangeEvent<HTMLSelectElement>);
              }
            }}
          >
            <Select.Trigger />
            <Select.Content>
              {props.options?.map((option) => (
                <Select.Item key={option.value} value={option.value.toString()}>
                  {option.label}
                </Select.Item>
              ))}
            </Select.Content>
          </Select.Root>
        ),
      }}
      css={{
        "& .rdp-today > .rdp-day_button": {
          border: "2px solid var(--gray-a9)",
          borderRadius: "var(--radius-4)",
          fontWeight: "var(--font-weight-bold)",
        },
      }}
      {...props}
    />
  );
};

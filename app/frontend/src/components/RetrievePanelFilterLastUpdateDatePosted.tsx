/**
 * @file RetrievePanelFilterLastUpdateDate.tsx
 *
 * The filter for last update date in the retrieval panel.
 */

import { Dispatch, SetStateAction } from "react";
import { DateRange } from "react-day-picker";
import { TrialFilters } from "../types";
import { RadixCalendar } from "./RadixCalendar";
import { Button, Flex, Popover } from "@radix-ui/themes";
import { MdCalendarMonth } from "react-icons/md";

interface RetrievePanelFilterLastUpdateDatePostedProps {
  filters: TrialFilters;
  setFilters: Dispatch<SetStateAction<TrialFilters>>;
}

export const RetrievePanelFilterLastUpdateDatePosted = ({
  filters,
  setFilters,
}: RetrievePanelFilterLastUpdateDatePostedProps) => {
  const range =
    filters.lastUpdateDatePosted === undefined
      ? undefined
      : {
          from: new Date(filters.lastUpdateDatePosted[0]),
          to: new Date(filters.lastUpdateDatePosted[1]),
        };

  const handler = (selectedRange?: DateRange) => {
    if (selectedRange?.from === undefined || selectedRange.to === undefined) {
      setFilters((prevFilters) => ({
        ...prevFilters,
        lastUpdateDatePosted: undefined,
      }));
      return;
    }

    const fromDate = selectedRange.from.getTime();
    const toDate = selectedRange.to.getTime();
    setFilters((prevFilters) => ({
      ...prevFilters,
      lastUpdateDatePosted: [fromDate, toDate],
    }));
  };
  const handleReset = () => {
    setFilters((prevFilters) => ({
      ...prevFilters,
      lastUpdateDatePosted: undefined,
    }));
  };

  return (
    <Flex direction="row" align="center" gap="4" width="100%">
      <Popover.Root>
        <Popover.Trigger>
          <Flex gap="2" height="var(--line-height-2)" asChild>
            <Button size="1" variant="outline">
              <MdCalendarMonth />
              {range === undefined
                ? "All"
                : `${range.from.toLocaleDateString()} ~ ${range.to.toLocaleDateString()}`}
            </Button>
          </Flex>
        </Popover.Trigger>
        <Popover.Content size="1">
          <RadixCalendar
            mode="range"
            selected={range}
            onSelect={handler}
            captionLayout="dropdown"
          />
        </Popover.Content>
      </Popover.Root>
      <Button
        size="1"
        variant="ghost"
        onClick={handleReset}
        style={{
          padding: "4px 12px",
          borderRadius: "4px",
          fontWeight: "bold",
        }}
      >
        Reset
      </Button>
    </Flex>
  );
};

/**
 * @file RetrievePanelFilterResultsDate.tsx
 *
 * The filter for results date in the retrieval panel.
 */

import { Dispatch, SetStateAction } from "react";
import { DateRange } from "react-day-picker";
import { TrialFilters } from "../types";
import { RadixCalendar } from "./RadixCalendar";
import { Button, Flex, Popover } from "@radix-ui/themes";
import { MdCalendarMonth } from "react-icons/md";

interface RetrievePanelFilterResultsDatePostedProps {
  filters: TrialFilters;
  setFilters: Dispatch<SetStateAction<TrialFilters>>;
}

export const RetrievePanelFilterResultsDatePosted = ({
  filters,
  setFilters,
}: RetrievePanelFilterResultsDatePostedProps) => {
  const range = filters.resultsDatePosted === undefined ? undefined : {
    from: new Date(filters.resultsDatePosted[0]),
    to: new Date(filters.resultsDatePosted[1]),
  }

  const handler = (selectedRange?: DateRange) => {
    if (selectedRange === undefined || selectedRange.from === undefined || selectedRange.to === undefined) {
      setFilters((prevFilters) => ({
        ...prevFilters,
        resultsDatePosted: undefined,
      }));
      return;
    }

    const fromDate = selectedRange.from.getTime();
    const toDate = selectedRange.to.getTime();
    setFilters((prevFilters) => ({
      ...prevFilters,
      resultsDatePosted: [fromDate, toDate],
    }));
  };

  return (
    <Popover.Root>
      <Popover.Trigger>
        <Flex gap="2" height="var(--line-height-2)" asChild>
          <Button size="1" variant="outline">
            <MdCalendarMonth />
            {(range === undefined) ? "All" : `${range.from.toLocaleDateString()} ~ ${range.to.toLocaleDateString()}`}
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
  );
};

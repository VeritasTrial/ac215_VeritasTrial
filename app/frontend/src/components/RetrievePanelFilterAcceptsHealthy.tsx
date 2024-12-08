/**
 * @file RetrievePanelFilterAcceptsHealthy.tsx
 *
 * The filter for accepting healthy patients or not in the retrieval panel.
 */

import { Dispatch, SetStateAction } from "react";
import { Flex, RadioGroup } from "@radix-ui/themes";
import { TrialFilters } from "../types";

interface RetrievePanelFilterAcceptsHealthyProps {
  filters: TrialFilters;
  setFilters: Dispatch<SetStateAction<TrialFilters>>;
}

export const RetrievePanelFilterAcceptsHealthy = ({
    filters,
    setFilters,
  }: RetrievePanelFilterAcceptsHealthyProps) => {
    const value =
      filters.acceptsHealthy === undefined
        ? "all"
        : filters.acceptsHealthy
        ? "True"
        : "False";
  
    const handler = (value: string) => {
      setFilters((prevFilters) => ({
        ...prevFilters,
        acceptsHealthy: value === "all" ? undefined : value === "True",
      }));
    };
  
    return (
      <RadioGroup.Root
        variant="surface"
        asChild
        value={value} 
        onValueChange={handler}
      >
        <Flex direction="row" gap="4">
          <RadioGroup.Item value="all">All</RadioGroup.Item>
          <RadioGroup.Item value="False">No</RadioGroup.Item>
          <RadioGroup.Item value="True">Yes</RadioGroup.Item>
        </Flex>
      </RadioGroup.Root>
    );
  };
  

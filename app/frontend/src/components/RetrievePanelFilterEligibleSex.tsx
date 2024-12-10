/**
 * @file RetrievePanelFilterEligibleSex.tsx
 *
 * The filter for eligible sex in the retrieval panel.
 */

import { Dispatch, SetStateAction } from "react";
import { Flex, RadioGroup } from "@radix-ui/themes";
import { TrialFilters } from "../types";

interface RetrievePanelFilterEligibleSexProps {
  filters: TrialFilters;
  setFilters: Dispatch<SetStateAction<TrialFilters>>;
}

export const RetrievePanelFilterEligibleSex = ({
  filters,
  setFilters,
}: RetrievePanelFilterEligibleSexProps) => {
  const value = filters.eligibleSex ?? "all";

  const handler = (value: string) => {
    setFilters((prevFilters) => ({
      ...prevFilters,
      eligibleSex: value === "all" ? undefined : value,
    }));
  };

  return (
    <RadioGroup.Root
      variant="surface"
      asChild
      value={value}
      onValueChange={handler}
    >
      <Flex direction="row" gapX="4">
        <RadioGroup.Item value="all">All</RadioGroup.Item>
        <RadioGroup.Item value="female">Female</RadioGroup.Item>
        <RadioGroup.Item value="male">Male</RadioGroup.Item>
      </Flex>
    </RadioGroup.Root>
  );
};

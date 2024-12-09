/**
 * @file RetrievePanelFilterPatientType.tsx
 *
 * The filter for accepting healthy patients or not in the retrieval panel.
 */

import { Dispatch, SetStateAction } from "react";
import { Checkbox, Flex } from "@radix-ui/themes";
import { TrialFilters } from "../types";

interface RetrievePanelFilterPatientTypeProps {
  filters: TrialFilters;
  setFilters: Dispatch<SetStateAction<TrialFilters>>;
}

export const RetrievePanelFilterPatientType = ({
  filters,
  setFilters,
}: RetrievePanelFilterPatientTypeProps) => {
  const value =
    filters.acceptsHealthy === undefined ? false : !filters.acceptsHealthy;

  const handler = (value: boolean | "indeterminate") => {
    setFilters((prevFilters) => ({
      ...prevFilters,
      acceptsHealthy: value === "indeterminate" ? true : !value,
    }));
  };

  return (
    <Flex gapX="2">
      <Checkbox checked={value} onCheckedChange={handler}></Checkbox>
      Exclude healthy patients
    </Flex>
  );
};

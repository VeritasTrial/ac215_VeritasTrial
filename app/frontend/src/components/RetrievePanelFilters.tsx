/**
 * @file RetrievePanelFilters.tsx
 *
 * The filters component in the retrieval panel.
 */

import { DataList } from "@radix-ui/themes";
import { Dispatch, SetStateAction } from "react";
import { TrialFilters } from "../types";
import { RetrievePanelFilterStudyType } from "./RetrievePanelFilterStudyType";

interface RetrievePanelFiltersProps {
  filters: TrialFilters;
  setFilters: Dispatch<SetStateAction<TrialFilters>>;
}

export const RetrievePanelFilters = ({
  filters,
  setFilters,
}: RetrievePanelFiltersProps) => {
  return (
    <DataList.Root
      size="2"
      css={{
        rowGap: "var(--space-2)",
        columnGap: "var(--space-6)",
        padding: "var(--space-1) 0",
      }}
    >
      <DataList.Item>
        <DataList.Label minWidth="0">Study type</DataList.Label>
        <DataList.Value>
          <RetrievePanelFilterStudyType
            filters={filters}
            setFilters={setFilters}
          />
        </DataList.Value>
      </DataList.Item>
    </DataList.Root>
  );
};

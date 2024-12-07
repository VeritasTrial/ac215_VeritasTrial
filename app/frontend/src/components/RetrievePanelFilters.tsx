/**
 * @file RetrievePanelFilters.tsx
 *
 * The filters component in the retrieval panel.
 */

import { DataList } from "@radix-ui/themes";
import { Dispatch, SetStateAction } from "react";
import { TrialFilters } from "../types";
import { RetrievePanelFilterStudyType } from "./RetrievePanelFilterStudyType";
import { RetrievePanelFilterStudyPhases } from "./RetrievePanelFilterStudyPhases";
import { RetrievePanelFilterAgeRange } from "./RetrievePanelFilterAgeRange";
import { RetrievePanelFilterEligibleSex } from "./RetrievePanelFilterEligibleSex";
import { RetrievePanelFilterLastUpdateDate } from "./RetrievePanelFilterLastUpdateDate";
import { RetrievePanelFilterResultsDate } from "./RetrievePanelFilterResultsDate";

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

      <DataList.Item>
        <DataList.Label minWidth="0">Study phases</DataList.Label>
        <DataList.Value>
          <RetrievePanelFilterStudyPhases
            filters={filters}
            setFilters={setFilters}
          />
        </DataList.Value>
      </DataList.Item>

      <DataList.Item>
        <DataList.Label minWidth="0">Age range</DataList.Label>
        <DataList.Value>
          <RetrievePanelFilterAgeRange
            filters={filters}
            setFilters={setFilters}
          />
        </DataList.Value>
      </DataList.Item>

      <DataList.Item>
        <DataList.Label minWidth="0">Eligible Sex</DataList.Label>
        <DataList.Value>
          <RetrievePanelFilterEligibleSex
            filters={filters}
            setFilters={setFilters}
          />
        </DataList.Value>
      </DataList.Item>

      <DataList.Item>
        <DataList.Label minWidth="0">Last Update Date</DataList.Label>
        <DataList.Value>
          <RetrievePanelFilterLastUpdateDate
            filters={filters}
            setFilters={setFilters}
          />
        </DataList.Value>
      </DataList.Item>

      <DataList.Item>
        <DataList.Label minWidth="0">Results Date</DataList.Label>
        <DataList.Value>
          <RetrievePanelFilterResultsDate
            filters={filters}
            setFilters={setFilters}
          />
        </DataList.Value>
      </DataList.Item>

    </DataList.Root>
  );
};
/**
 * @file types.ts
 *
 * This file defines custom types and interfaces for the application.
 */

import { ReactNode } from "react";

/**
 * The appearance type.
 */
export type ApperanceType = "dark" | "light";

/**
 * Wrap an API response to distinguish success and failure.
 */
export type WrapAPI<T> = { payload: T } | { error: string };

/**
 * Metainfo of a trial, used specifically for frontend display.
 */
export interface MetaInfo {
  title: string;
}

/**
 * Chat display interface.
 */
export interface ChatDisplay {
  /** Whether the message is from the user, otherwise it is from the bot. */
  fromUser: boolean;
  /** The React element to display for the message. */
  element: ReactNode;
}

/**
 * Type of the function that updates messages.
 */
export type UpdateMessagesFunction = (
  prevMessages: ChatDisplay[],
) => ChatDisplay[];

/* ==========================================================================
 *   THE FOLLOWING ARE MIRROR DEFINITIONS OF BACKEND TYPES. CHECK OUT THE
 *   BACKEND API FOR REFERENCE.
 * ========================================================================== */

export type ModelType = "gemini-1.5-flash-001" | "6894888983713546240";

export interface TrialMetadataMeasureOutcomeType {
  measure: string;
  description: string;
  timeFrame: string;
}

export interface TrialMetadataInterventionType {
  type: string;
  name: string;
  description: string;
}

export interface TrialMetadataReferenceType {
  pmid: string;
  citation: string;
}

export interface TrialMetadataDocumentType {
  url: string;
  size: number;
}

export interface TrialMetadataType {
  shortTitle: string;
  longTitle: string;
  organization: string;
  submitDate: string;
  submitDateQc: string;
  submitDatePosted: string;
  resultsDate: string;
  resultsDateQc: string;
  resultsDatePosted: string;
  lastUpdateDate: string;
  lastUpdateDatePosted: string;
  verifyDate: string;
  sponsor: string;
  collaborators: string[];
  summary: string;
  details: string;
  conditions: string[];
  studyPhases: string;
  studyType: string;
  enrollmentCount: number;
  allocation: string;
  interventionModel: string;
  observationalModel: string;
  primaryPurpose: string;
  whoMasked: string;
  interventions: TrialMetadataInterventionType[];
  primaryMeasureOutcomes: TrialMetadataMeasureOutcomeType[];
  secondaryMeasureOutcomes: TrialMetadataMeasureOutcomeType[];
  otherMeasureOutcomes: TrialMetadataMeasureOutcomeType[];
  minAge: number;
  maxAge: number;
  eligibleSex: string;
  acceptsHealthy: boolean;
  inclusionCriteria: string;
  exclusionCriteria: string;
  officials: string[];
  locations: string[];
  references: TrialMetadataReferenceType[];
  documents: TrialMetadataDocumentType[];
}

export interface APIHeartbeatResponseType {
  timestamp: number;
}

export interface APIRetrieveResponseType {
  ids: string[];
  documents: string[];
}

export interface APIMetaResponseType {
  metadata: TrialMetadataType;
}

export interface APIChatResponseType {
  response: string;
}

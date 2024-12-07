/**
 * @file MessageDocs.tsx
 *
 * This file contains the message component that displays the references and
 * related documentations of a trial.
 */

import { Code, Flex, Text } from "@radix-ui/themes";
import {
  TrialMetadataDocumentType,
  TrialMetadataReferenceType,
} from "../types";
import { ExternalLink } from "./ExternalLink";
import { PUBMED_URL } from "../consts";
import { CopyButton } from "./CopyButton";

interface MessageDocsProps {
  references: TrialMetadataReferenceType[];
  documents: TrialMetadataDocumentType[];
}

export const MessageDocs = ({ references, documents }: MessageDocsProps) => {
  return (
    <Flex direction="column" gap="4">
      {/* References */}
      {references.length > 0 && (
        <Flex direction="column" gap="3">
          <Text size="2" weight="medium">
            References
          </Text>
          {references.map((ref) => (
            <Flex
              key={ref.pmid}
              align="center"
              justify="between"
              gap="2"
              pr="1"
            >
              <ExternalLink href={`${PUBMED_URL}/${ref.pmid}`} size="2">
                {ref.citation}
              </ExternalLink>{" "}
              <CopyButton text={ref.citation} />
            </Flex>
          ))}
        </Flex>
      )}
      {/* Related documents */}
      {documents.length > 0 && (
        <Flex direction="column" gap="3">
          <Text size="2" weight="medium">
            Related Documents
          </Text>
          {documents.map((doc) => (
            <Flex key={doc.url} align="center" justify="between" gap="2" pr="1">
              <ExternalLink href={doc.url} size="2">
                {doc.url.split("/").pop()}
              </ExternalLink>{" "}
              <Code variant="ghost" color="gray" size="2">
                {Math.round(doc.size / 1024)}KB
              </Code>
            </Flex>
          ))}
        </Flex>
      )}
      {references.length === 0 && documents.length === 0 && (
        <Text size="2" weight="medium" color="red">
          No references found.
        </Text>
      )}
    </Flex>
  );
};

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
    <Flex direction="column" gap="3">
      {/* References */}
      {references.length > 0 ? (
        <Flex direction="column" gap="1">
          <Text size="2" weight="medium" mb="1">
            References
          </Text>
          {references.map((ref) => (
            <Flex align="center" justify="between" gap="2" pr="1">
              <ExternalLink
                key={ref.pmid}
                href={`${PUBMED_URL}/${ref.pmid}`}
                size="2"
              >
                {ref.citation}
              </ExternalLink>{" "}
              <CopyButton text={ref.citation} />
            </Flex>
          ))}
        </Flex>
      ) : (
        <Text size="2" weight="medium" color="red">
          No references found.
        </Text>
      )}
      {/* Related documents */}
      {documents.length > 0 ? (
        <Flex direction="column" gap="1">
          <Text size="2" weight="medium" mb="1">
            Related Documents
          </Text>
          {documents.map((doc) => (
            <Flex align="center" justify="between" gap="2" pr="1">
              <ExternalLink key={doc.url} href={doc.url} size="2">
                {doc.url.split("/").pop()}
              </ExternalLink>{" "}
              <Code variant="ghost" color="gray" size="2">
                {Math.round(doc.size / 1024)}KB
              </Code>
            </Flex>
          ))}
        </Flex>
      ) : (
        <Text size="2" weight="medium" color="red">
          No related documents found.
        </Text>
      )}
    </Flex>
  );
};

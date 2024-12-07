/**
 * @file RadixMarkdown.tsx
 *
 * Markdown renderer using Radix UI components.
 */

import {
  Blockquote,
  Box,
  Code,
  Em,
  Heading,
  Link,
  ScrollArea,
  Separator,
  Strong,
  Table,
  Text,
  TextProps,
} from "@radix-ui/themes";
import Markdown from "react-markdown";
import remarkGfm from "remark-gfm";
import rehypeRaw from "rehype-raw";
import rehypeSanitize from "rehype-sanitize";

interface RadixMarkdownProps {
  text: string;
  size?: TextProps["size"];
}

const headingCss = {
  paddingTop: "var(--space-4)",
  paddingBottom: "var(--space-3)",
  ":first-child": { paddingTop: 0 },
};
const boxCss = {
  marginBottom: "var(--space-3)",
  ":first-child": { marginTop: 0 },
  ":last-child": { marginBottom: 0 },
};

export const RadixMarkdown = ({ text, size }: RadixMarkdownProps) => {
  return (
    <Text size={size} as="div">
      <Markdown
        remarkPlugins={[remarkGfm]}
        rehypePlugins={[rehypeRaw, rehypeSanitize]}
        components={{
          // Text-based components
          span: (props) => {
            const { node: _, ...rest } = props;
            return <Text {...rest}></Text>;
          },
          a: (props) => {
            const { node: _, ...rest } = props;
            return <Link {...rest}></Link>;
          },
          em: (props) => {
            const { node: _, ...rest } = props;
            return <Em {...rest}></Em>;
          },
          strong: (props) => {
            const { node: _, ...rest } = props;
            return <Strong {...rest}></Strong>;
          },
          code: (props) => {
            const { node: _, ...rest } = props;
            return <Code variant="ghost" {...rest}></Code>;
          },
          label: (props) => {
            const { node: _, ...rest } = props;
            return <Text as="label" {...rest}></Text>;
          },
          // Block-based components
          div: (props) => {
            const { node: _, ...rest } = props;
            return <Text as="div" {...rest}></Text>;
          },
          p: (props) => {
            const { node: _, ...rest } = props;
            return (
              <Box css={boxCss} asChild>
                <Text as="p" {...rest}></Text>
              </Box>
            );
          },
          blockquote: (props) => {
            const { node: _, ...rest } = props;
            return (
              <Box css={boxCss} asChild>
                <Blockquote {...rest}></Blockquote>
              </Box>
            );
          },
          pre: (props) => {
            const { node: _, ...rest } = props;
            return (
              <ScrollArea scrollbars="horizontal" asChild>
                <Box
                  as="pre"
                  p="2"
                  css={{
                    whiteSpace: "pre",
                    backgroundColor: "var(--gray-a2)",
                    borderRadius: "var(--radius-3)",
                    ...boxCss,
                  }}
                  {...rest}
                ></Box>
              </ScrollArea>
            );
          },
          // Heading components
          h1: (props) => {
            const { node: _, ...rest } = props;
            return <Heading as="h1" css={headingCss} {...rest}></Heading>;
          },
          h2: (props) => {
            const { node: _, ...rest } = props;
            return <Heading as="h2" css={headingCss} {...rest}></Heading>;
          },
          h3: (props) => {
            const { node: _, ...rest } = props;
            return <Heading as="h3" css={headingCss} {...rest}></Heading>;
          },
          h4: (props) => {
            const { node: _, ...rest } = props;
            return <Heading as="h4" css={headingCss} {...rest}></Heading>;
          },
          h5: (props) => {
            const { node: _, ...rest } = props;
            return <Heading as="h5" css={headingCss} {...rest}></Heading>;
          },
          h6: (props) => {
            const { node: _, ...rest } = props;
            return <Heading as="h6" css={headingCss} {...rest}></Heading>;
          },
          // List components
          ul: (props) => {
            const { node: _, ...rest } = props;
            return <Box as="ul" pl="3" css={boxCss} {...rest}></Box>;
          },
          ol: (props) => {
            const { node: _, ...rest } = props;
            return <Box as="ol" pl="3" css={boxCss} {...rest}></Box>;
          },
          // Table components
          table: (props) => {
            const { node: _, ...rest } = props;
            return (
              <Box css={boxCss} asChild>
                <Table.Root size="1" variant="ghost" {...rest}></Table.Root>
              </Box>
            );
          },
          thead: (props) => {
            const { node: _, ...rest } = props;
            return <Table.Header {...rest}></Table.Header>;
          },
          tbody: (props) => {
            const { node: _, ...rest } = props;
            return <Table.Body {...rest}></Table.Body>;
          },
          tr: (props) => {
            const { node: _, ...rest } = props;
            return <Table.Row {...rest}></Table.Row>;
          },
          th: (props) => {
            const { node: _, ...rest } = props;
            return <Table.ColumnHeaderCell {...rest}></Table.ColumnHeaderCell>;
          },
          td: (props) => {
            const { node: _, ...rest } = props;
            return <Table.Cell {...rest}></Table.Cell>;
          },
          // Misc components
          hr: (props) => {
            const { node: _, ...rest } = props;
            return (
              <Box css={boxCss} asChild>
                <Separator size="4" {...rest}></Separator>
              </Box>
            );
          },
        }}
      >
        {text}
      </Markdown>
    </Text>
  );
};

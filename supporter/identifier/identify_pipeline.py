from supporter.identifier.base_identifier import BaseIdentifier, IdentifyResult


def merge_identify_results(results1: list[IdentifyResult], results2: list[IdentifyResult]) -> list[IdentifyResult]:
    """
    merge two lists of IdentifyResults such that there is no overlap between the two lists.
    Note that this function will keep the result in results1 and clear the overlapping result in results2.

    Args:
        results1: IdentifyResult list 1
        results2: IdentifyResult list 2s

    Returns:
        merged results
    """

    def check_overlap(span: tuple[int, int], results: list[IdentifyResult]) -> bool:
        s1, e1 = span[0], span[1]
        for result in results:
            s2, e2 = result.start_inclusive, result.end_exclusive
            _s1, _e1, _s2, _e2 = (s1, e1, s2, e2) if s1 < s2 else (s2, e2, s1, e1)
            if _s2 < _e1:
                return True
        return False

    final_results = results1.copy()
    for result in results2:
        span = (result.start_inclusive, result.end_exclusive)
        if not check_overlap(span, final_results):
            final_results.append(result)
    return final_results


class IdentifyPipeline:
    identifier_sequence: list[BaseIdentifier] = list()

    def __init__(self, *identifiers: BaseIdentifier):
        self.identifier_sequence = list(identifiers)

    def execute(self, article: str) -> list[IdentifyResult]:
        """
        follow the sequence of identifier, and merge the results.
        Note that the result before will NOT be overwritten.
        Instead, the result after will be discarded if it overlapped with the result before.

        Args:
            article: the article to be identified.

        Returns:
            the identify results.
        """
        results = list()

        for identifier in self.identifier_sequence:
            identify_results = identifier.identify(article)
            results = merge_identify_results(results, identify_results)

        return results

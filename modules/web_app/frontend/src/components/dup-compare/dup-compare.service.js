import { of } from 'rxjs'

class DupCompareService {
  getSimilarityResults = (sourceContent, targetContent) => {
    const sourceParagraphs = sourceContent.split('\n')
    const targetParagraphs = targetContent.split('\n')
    const minLength = sourceParagraphs.length < targetParagraphs.length
      ? sourceParagraphs.length
      : targetParagraphs.length
    return of({
      pairs: [...Array(minLength)].map((_, idx) => ({
        source: sourceParagraphs[idx],
        target: targetParagraphs[idx]
      }))
    })
  }
}

export default DupCompareService